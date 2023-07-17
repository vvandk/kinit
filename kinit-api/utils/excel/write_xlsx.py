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
import datetime
import hashlib
import os.path
import random
import xlsxwriter
from application.settings import TEMP_DIR, TEMP_URL


class WriteXlsx:
    """
    写入xlsx文件
    """

    def __init__(self, filename: str = None, sheet_name: str = "sheet1"):
        date = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
        file_dir = os.path.join(TEMP_DIR, date)
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        if not filename:
            filename = hashlib.md5(str(random.random()).encode()).hexdigest()
        self.file_url = f"{TEMP_URL}/{date}/{filename}.xlsx"
        self.filename = os.path.join(TEMP_DIR, date, filename + ".xlsx")
        self.sheet_name = sheet_name
        self.wb = None
        self.sheet = None

    def create_excel(self) -> None:
        """
        创建 excel 文件
        """

        self.wb = xlsxwriter.Workbook(self.filename)
        self.sheet = self.wb.add_worksheet(self.sheet_name)

    def generate_template(self, headers: list[dict] = None, max_row: int = 101) -> None:
        """
        生成模板
        :param headers: 表头
        :param max_row: 设置下拉列表至最大行
        :return: 文件链接地址
        """
        self.create_excel()
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
        # self.sheet.set_row(row_number, 25)
        self.sheet.set_default_row(25)

    def close(self) -> None:
        """
        关闭文件
        """
        self.wb.close()
