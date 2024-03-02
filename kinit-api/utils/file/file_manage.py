# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/12/5 8:45
# @File           : file_manage.py
# @IDE            : PyCharm
# @desc           : 保存图片到本地

import asyncio
import io
import os
import zipfile
from application.settings import STATIC_ROOT, BASE_DIR, STATIC_URL
from fastapi import UploadFile
import sys
from core.exception import CustomException
from utils.file.file_base import FileBase
from aiopathlib import AsyncPath
import aioshutil


class FileManage(FileBase):
    """
    上传文件管理
    """

    def __init__(self, file: UploadFile, path: str):
        self.path = self.generate_static_file_path(path, file.filename)
        self.file = file

    async def save_image_local(self, accept: list = None) -> dict:
        """
        保存图片文件到本地
        :param accept:
        :return:
        """
        if accept is None:
            accept = self.IMAGE_ACCEPT
        await self.validate_file(self.file, max_size=5, mime_types=accept)
        return await self.async_save_local()

    async def save_audio_local(self, accept: list = None) -> dict:
        """
        保存音频文件到本地
        :param accept:
        :return:
        """
        if accept is None:
            accept = self.AUDIO_ACCEPT
        await self.validate_file(self.file, max_size=50, mime_types=accept)
        return await self.async_save_local()

    async def save_video_local(self, accept: list = None) -> dict:
        """
        保存视频文件到本地
        :param accept:
        :return:
        """
        if accept is None:
            accept = self.VIDEO_ACCEPT
        await self.validate_file(self.file, max_size=100, mime_types=accept)
        return await self.async_save_local()

    async def async_save_local(self) -> dict:
        """
        保存文件到本地
        :return: 示例：
        {
            'local_path': 'D:\\project\\kinit_dev\\kinit-api\\static\\system\\20240301\\1709303205HuYB3mrC.png',
            'remote_path': '/media/system/20240301/1709303205HuYB3mrC.png'
        }
        """
        path = AsyncPath(self.path)
        if sys.platform == "win32":
            path = AsyncPath(self.path.replace("/", "\\"))
        if not await path.parent.exists():
            await path.parent.mkdir(parents=True, exist_ok=True)
        await path.write_bytes(await self.file.read())
        return {
            "local_path": str(path),
            "remote_path": STATIC_URL + str(path).replace(STATIC_ROOT, '').replace("\\", '/')
        }

    @classmethod
    async def async_save_temp_file(cls, file: UploadFile) -> str:
        """
        保存临时文件
        :param file:
        :return:
        """
        temp_file_path = await cls.async_generate_temp_file_path(file.filename)
        await AsyncPath(temp_file_path).write_bytes(await file.read())
        return temp_file_path

    @classmethod
    async def unzip(cls, file: UploadFile, dir_path: str) -> str:
        """
        解压 zip 压缩包
        :param file:
        :param dir_path: 解压路径
        :return:
        """
        if file.content_type != "application/x-zip-compressed":
            raise CustomException("上传文件类型错误，必须是 zip 压缩包格式！")
        # 读取上传的文件内容
        contents = await file.read()
        # 将文件内容转换为字节流
        zip_stream = io.BytesIO(contents)
        # 使用zipfile库解压字节流
        with zipfile.ZipFile(zip_stream, "r") as zip_ref:
            zip_ref.extractall(dir_path)
        return dir_path

    @staticmethod
    async def async_copy_file(src: str, dst: str) -> None:
        """
        异步复制文件
        根目录为项目根目录，传过来的文件路径均为相对路径
        :param src: 原始文件
        :param dst: 目标路径。绝对路径
        """
        if src[0] == "/":
            src = src.lstrip("/")
        src = AsyncPath(BASE_DIR) / src
        if not await src.exists():
            raise CustomException(f"{src} 源文件不存在！")
        dst = AsyncPath(dst)
        if not await dst.parent.exists():
            await dst.parent.mkdir(parents=True, exist_ok=True)
        await aioshutil.copyfile(src, dst)

    @staticmethod
    async def async_copy_dir(src: str, dst: str, dirs_exist_ok: bool = True) -> None:
        """
        复制目录
        :param src: 源目录
        :param dst: 目标目录
        :param dirs_exist_ok: 是否覆盖
        """
        if not os.path.exists(dst):
            raise CustomException("目标目录不存在！")
        await aioshutil.copytree(src, dst, dirs_exist_ok=dirs_exist_ok)
