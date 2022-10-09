# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/12/5 8:45
# @File           : save_file.py
# @IDE            : PyCharm
# @desc           : 保存图片到本地

from datetime import datetime
import os
from application.settings import TEMP_DIR
from fastapi import UploadFile


def save_tmp_file(file: UploadFile, data):
    """
    保存临时文件
    """
    date = datetime.strftime(datetime.now(), "%Y%m%d")
    file_dir = os.path.join(TEMP_DIR, date)
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    with open(os.path.join(file_dir, file.filename), "wb") as f:
        f.write(data)
