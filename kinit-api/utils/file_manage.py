# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/12/5 8:45
# @File           : file_manage.py
# @IDE            : PyCharm
# @desc           : 保存图片到本地

import datetime
import os
import shutil
from application.settings import TEMP_DIR, STATIC_ROOT, BASE_DIR, STATIC_DIR, STATIC_URL
from fastapi import UploadFile
import sys
from core.exception import CustomException
from utils import status
import uuid


class FileManage:
    """
    上传文件管理
    """

    image_accept = ["image/png", "image/jpeg", "image/gif", "image/x-icon"]

    def __init__(self, file: UploadFile, path: str):
        if path[0] == "/":
            path = path[1:]
        if path[-1] == "/":
            path = path[:-1]
        full_date = datetime.datetime.now().date()
        filename = str(int(datetime.datetime.now().timestamp())) + str(uuid.uuid4())[:8]
        self.path = f"{path}/{full_date}/{filename}{os.path.splitext(file.filename)[-1]}"
        self.file = file

    async def save_image_local(self, accept: list = None) -> dict:
        """
        保存图片文件到本地
        """
        if accept is None:
            accept = self.image_accept
        if self.file.content_type not in accept:
            raise CustomException(f"上传图片必须是 {'/'.join(accept)} 格式!", status.HTTP_ERROR)
        return await self.save_local()

    async def save_local(self) -> dict:
        """
        保存文件到本地
        """
        path = self.path
        if sys.platform == "win32":
            path = self.path.replace("/", "\\")
        save_path = os.path.join(STATIC_ROOT, path)
        if not os.path.exists(os.path.dirname(save_path)):
            os.mkdir(os.path.dirname(save_path))
        with open(save_path, "wb") as f:
            f.write(await self.file.read())
        return {
            "local_path": f"{STATIC_DIR}/{self.path}",
            "remote_path": f"{STATIC_URL}/{self.path}"
        }

    @staticmethod
    async def save_tmp_file(file: UploadFile) -> str:
        """
        保存临时文件
        """
        date = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
        file_dir = os.path.join(TEMP_DIR, date)
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        filename = os.path.join(file_dir, str(int(datetime.datetime.now().timestamp())) + file.filename)
        with open(filename, "wb") as f:
            f.write(await file.read())
        return filename

    @staticmethod
    def copy(src: str, dst: str) -> None:
        """
        复制文件
        根目录为项目根目录，传过来的文件路径均为相对路径

        @param src: 原始文件
        @param dst: 目标路径。绝对路径
        """
        if src[0] == "/":
            src = src.lstrip("/")
        if sys.platform == "win32":
            src = src.replace("/", "\\")
            dst = dst.replace("/", "\\")
        src = os.path.join(BASE_DIR, src)
        if not os.path.exists(os.path.dirname(dst)):
            os.mkdir(os.path.dirname(dst))
        shutil.copyfile(src, dst)


if __name__ == '__main__':
    print()
