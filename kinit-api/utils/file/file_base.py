#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/12/12 14:31 
# @File           : file_base.py
# @IDE            : PyCharm
# @desc           : 简要说明

import datetime
import os
from pathlib import Path

from aiopathlib import AsyncPath
from fastapi import UploadFile
from application.settings import TEMP_DIR
from core.exception import CustomException
from utils import status
from utils.tools import generate_string


class FileBase:

    IMAGE_ACCEPT = ["image/png", "image/jpeg", "image/gif", "image/x-icon"]
    VIDEO_ACCEPT = ["video/mp4", "video/mpeg"]
    AUDIO_ACCEPT = ["audio/wav", "audio/mp3", "audio/m4a", "audio/wma", "audio/ogg", "audio/mpeg", "audio/x-wav"]
    ALL_ACCEPT = [*IMAGE_ACCEPT, *VIDEO_ACCEPT, *AUDIO_ACCEPT]

    @classmethod
    def generate_static_file_path(cls, path: str, filename: str) -> str:
        """
        生成文件路径
        :param path: static 指定目录类别
        :param filename: 文件名称
        :return:
        """
        path = path.replace("\\", "/")
        if path[0] == "/":
            path = path[1:]
        if path[-1] == "/":
            path = path[:-1]
        today = str(int((datetime.datetime.now().replace(hour=0, minute=0, second=0)).timestamp()))
        _filename = str(int(datetime.datetime.now().timestamp())) + str(generate_string(8))
        return f"{path}/{today}/{_filename}{os.path.splitext(filename)[-1]}"

    @classmethod
    def generate_temp_file_path(cls, filename: str) -> str:
        """
        生成临时文件路径
        :param filename: 文件名称
        :return:
        """
        return f"{cls.generate_temp_dir_path()}/{filename}"

    @classmethod
    def generate_temp_dir_path(cls) -> str:
        """
        生成临时目录路径
        :return:
        """
        date = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
        file_dir = Path(TEMP_DIR) / date
        path = file_dir / (generate_string(4) + str(int(datetime.datetime.now().timestamp())))
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return str(path).replace("\\", "/")

    @classmethod
    async def async_generate_temp_file_path(cls, filename: str) -> str:
        """
        生成临时文件路径
        :param filename: 文件名称
        :return:
        """
        return f"{await cls.async_generate_temp_dir_path()}/{filename}"

    @classmethod
    async def async_generate_temp_dir_path(cls) -> str:
        """
        生成临时目录路径
        :return:
        """
        date = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
        file_dir = AsyncPath(TEMP_DIR) / date
        path = file_dir / (generate_string(4) + str(int(datetime.datetime.now().timestamp())))
        if not await path.exists():
            await path.mkdir(parents=True, exist_ok=True)
        return str(path).replace("\\", "/")

    @classmethod
    async def validate_file(cls, file: UploadFile, max_size: int = None, mime_types: list = None) -> bool:
        """
        验证文件是否符合格式

        :param file: 文件
        :param max_size: 文件最大值，单位 MB
        :param mime_types: 支持的文件类型
        """
        if max_size:
            size = len(await file.read()) / 1024 / 1024
            if size > max_size:
                raise CustomException(f"上传文件过大，不能超过{max_size}MB", status.HTTP_ERROR)
            await file.seek(0)
        if mime_types:
            if file.content_type not in mime_types:
                raise CustomException(f"上传文件格式错误，只支持 {'/'.join(mime_types)} 格式!", status.HTTP_ERROR)
        return True
