#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/11/11 12:01 
# @File           : write_xlsx.py
# @IDE            : PyCharm
# @desc           : 简要说明

"""
XlsxWriter：https://github.com/jmcnamara/XlsxWriter
博客教程：https://blog.csdn.net/lemonbit/article/details/113855768
"""

import os.path
import xlsxwriter
from typing import List
from application.settings import STATIC_ROOT, STATIC_URL
from utils.file.file_base import FileBase
from pathlib import Path


class WriteXlsx:
    """
    写入xlsx文件
    """

    def __init__(self):
        self.file_path = None
        self.sheet_name = None
        self.wb = None
        self.sheet = None

    def create_excel(self, file_path: str = None, sheet_name: str = "sheet1", save_static: bool = False) -> None:
        """
        创建 excel 文件
        :param file_path: 文件绝对路径或相对路径
        :param sheet_name: sheet 名称
        :param save_static: 保存方式 static 静态资源或者临时文件
        :return:
        """
        if not file_path:
            if save_static:
                self.file_path = FileBase.generate_static_file_path(path="write_xlsx", suffix="xlsx")
            else:
                self.file_path = FileBase.generate_temp_file_path(suffix="xlsx")
        elif not os.path.isabs(file_path):
            if save_static:
                self.file_path = FileBase.generate_static_file_path(path="write_xlsx", filename=file_path)
            else:
                self.file_path = FileBase.generate_temp_file_path(filename=file_path)
        else:
            self.file_path = file_path
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
        self.sheet_name = sheet_name
        self.wb = xlsxwriter.Workbook(self.file_path)
        self.sheet = self.wb.add_worksheet(sheet_name)

    def generate_template(self, headers: List[dict] = None, max_row: int = 101) -> None:
        """
        生成模板
        :param headers: 表头
        :param max_row: 设置下拉列表至最大行
        :return: 文件链接地址
        """
        max_row = max_row + 100
        for index, field in enumerate(headers):
            font_format = {
                'bold': False,  # 字体加粗
                'align': 'center',  # 水平位置设置：居中
                'valign': 'vcenter',  # 垂直位置设置，居中
                'font_size': 11,  # '字体大小设置'
            }
            if field.get("required", False):
                # 设置单元格必填样式
                field["label"] = "* " + field["label"]
                font_format["font_color"] = "red"
            if field.get("options", False):
                # 添加数据验证，下拉列表
                validate = {'validate': 'list', 'source': [item.get("label") for item in field.get("options", [])]}
                self.sheet.data_validation(1, index, max_row, index, validate)
            cell_format = self.wb.add_format(font_format)
            self.sheet.write(0, index, field.get("label"), cell_format)
        # 设置列宽
        self.sheet.set_column(0, len(headers) - 1, 22)
        # 设置行高
        self.sheet.set_row(0, 25)

    def write_list(self, rows: list, start_row: int = 1) -> None:
        """
        写入 excel文件

        :param rows: 行数据集
        :param start_row: 开始行
        """
        font_format = {
            'bold': False,  # 字体加粗
            'align': 'center',  # 水平位置设置：居中
            'valign': 'vcenter',  # 垂直位置设置，居中
            'font_size': 11,  # '字体大小设置'
        }
        cell_format = self.wb.add_format(font_format)
        for index, row in enumerate(rows):
            row_number = index+start_row
            self.sheet.write_row(row_number, 0, row, cell_format)
        # 设置列宽
        self.sheet.set_column(0, len(rows[0]) - 1, 22)
        # 设置行高
        self.sheet.set_default_row(25)

    def close(self) -> None:
        """
        关闭文件
        """
        self.wb.close()

    def get_file_url(self) -> str:
        """
        获取访问文件的 url
        :return:
        """
        if not self.file_path:
            raise ValueError("还未创建文件，请先创建 excel 文件！")
        assert isinstance(self.file_path, str)
        if self.file_path.startswith(STATIC_ROOT):
            return self.file_path.replace(STATIC_ROOT, STATIC_URL)
        else:
            print("write_xlsx 生成文件：", self.file_path)
            raise ValueError("生成文件为临时文件，无法访问！")

