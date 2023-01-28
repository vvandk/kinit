#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/4/28 22:32 
# @File           : aliyun_oss.py
# @IDE            : PyCharm
# @desc           : 阿里云对象存储

import os.path
from fastapi import UploadFile
from pydantic import BaseModel
import oss2  # 安装依赖库：pip install oss2
from oss2.models import PutObjectResult
from core.logger import logger
from utils.file.compress.cpressJPG import compress_jpg_png
from utils.file.file_manage import FileManage
from utils.file.file_base import FileBase


class BucketConf(BaseModel):
    accessKeyId: str
    accessKeySecret: str
    endpoint: str
    bucket: str
    baseUrl: str


class AliyunOSS(FileBase):
    """
    阿里云对象存储

    常见报错：https://help.aliyun.com/document_detail/185228.htm?spm=a2c4g.11186623.0.0.6de530e5pxNK76#concept-1957777
    官方文档：https://help.aliyun.com/document_detail/32026.html

    使用Python SDK时，大部分操作都是通过oss2.Service和oss2.Bucket两个类进行。
    oss2.Service类用于列举存储空间。
    oss2.Bucket类用于上传、下载、删除文件以及对存储空间进行各种配置。
    """

    def __init__(self, bucket: BucketConf):
        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        auth = oss2.Auth(bucket.accessKeyId, bucket.accessKeySecret)
        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称。
        self.bucket = oss2.Bucket(auth, bucket.endpoint, bucket.bucket)
        self.baseUrl = bucket.baseUrl

    async def upload_image(self, path: str, file: UploadFile, compress: bool = False) -> str:
        """
        上传图片

        @param path: path由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
        @param file: 文件对象
        @param compress: 是否压缩该文件
        @return: 上传后的文件oss链接
        """
        path = self.generate_path(path, file.filename)
        if compress:
            # 压缩图片
            file_path = await FileManage.save_tmp_file(file)
            new_file = compress_jpg_png(file_path, originpath=os.path.abspath(file_path))
            with open(new_file, "rb") as f:
                file_data = f.read()
        else:
            file_data = await file.read()
        result = self.bucket.put_object(path, file_data)
        assert isinstance(result, PutObjectResult)
        if result.status != 200:
            logger.error(f"图片上传到OSS失败，状态码：{result.status}")
            print("图片上传路径", path)
            print(f"图片上传到OSS失败，状态码：{result.status}")
            return ""
        return self.baseUrl + path

    async def upload_file(self, path: str, file: UploadFile) -> str:
        """
        上传文件

        @param path: path由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
        @param file: 文件对象
        @return: 上传后的文件oss链接
        """
        path = self.generate_path(path, file.filename)
        file_data = await file.read()
        result = self.bucket.put_object(path, file_data)
        assert isinstance(result, PutObjectResult)
        if result.status != 200:
            logger.error(f"文件上传到OSS失败，状态码：{result.status}")
            return ""
        return self.baseUrl + path
