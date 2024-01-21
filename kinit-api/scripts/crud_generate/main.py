#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/12/9 15:27
# @File           : main.py
# @IDE            : PyCharm
# @desc           : 简要说明

import os.path
import sys
from typing import Type
from application.settings import BASE_DIR
import inspect
from pathlib import Path
from core.database import Base
from scripts.crud_generate.utils.generate_base import GenerateBase
from scripts.crud_generate.utils.schema_generate import SchemaGenerate
from scripts.crud_generate.utils.params_generate import ParamsGenerate
from scripts.crud_generate.utils.dal_generate import DalGenerate
from scripts.crud_generate.utils.view_generate import ViewGenerate


class CrudGenerate(GenerateBase):

    APPS_ROOT = os.path.join(BASE_DIR, "apps")
    SCRIPT_DIR = os.path.join(BASE_DIR, 'scripts', 'crud_generate')

    def __init__(self, model: Type[Base], zh_name: str, en_name: str = None):
        """
        初始化工作
        :param model: 提前定义好的 ORM 模型
        :param zh_name: 功能中文名称，主要用于描述、注释
        :param en_name: 功能英文名称，主要用于 schema、param 文件命名，以及它们的 class 命名，dal、url 命名，默认使用 model class
        en_name 例子：
            如果 en_name 由多个单词组成那么请使用 _ 下划线拼接
            在命名文件名称时，会执行使用 _ 下划线名称
            在命名 class 名称时，会将下划线名称转换为大驼峰命名（CamelCase）
            在命名 url 时，会将下划线转换为 /
        """
        self.model = model
        self.zh_name = zh_name
        # model 文件的地址
        self.model_file_path = Path(inspect.getfile(sys.modules[model.__module__]))
        # model 文件 app 路径
        self.app_dir_path = self.model_file_path.parent.parent
        # schemas 目录地址
        self.schemas_dir_path = self.app_dir_path / "schemas"
        # params 目录地址
        self.params_dir_path = self.app_dir_path / "params"
        # crud 文件地址
        self.crud_file_path = self.app_dir_path / "crud.py"
        # view 文件地址
        self.view_file_path = self.app_dir_path / "views.py"

        if en_name:
            self.en_name = en_name
        else:
            self.en_name = self.model.__name__

        self.schema_file_path = self.schemas_dir_path / f"{self.en_name}.py"
        self.param_file_path = self.params_dir_path / f"{self.en_name}.py"

        self.base_class_name = self.snake_to_camel(self.en_name)
        self.schema_simple_out_class_name = f"{self.base_class_name}SimpleOut"
        self.dal_class_name = f"{self.base_class_name}Dal"
        self.param_class_name = f"{self.base_class_name}Params"

    def generate_codes(self):
        """
        生成代码， 不做实际操作，只是将代码打印出来
        :return:
        """
        print(f"==========================={self.schema_file_path} 代码内容=================================")
        schema = SchemaGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.schema_file_path,
            self.schemas_dir_path,
            self.base_class_name,
            self.schema_simple_out_class_name
        )
        print(schema.generate_code())

        print(f"==========================={self.dal_class_name} 代码内容=================================")
        dal = DalGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.dal_class_name,
            self.schema_simple_out_class_name
        )
        print(dal.generate_code())

        print(f"==========================={self.param_file_path} 代码内容=================================")
        params = ParamsGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.params_dir_path,
            self.param_file_path,
            self.param_class_name
        )
        print(params.generate_code())

        print(f"==========================={self.view_file_path} 代码内容=================================")
        view = ViewGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.base_class_name,
            self.schema_simple_out_class_name,
            self.dal_class_name,
            self.param_class_name
        )
        print(view.generate_code())

    def main(self):
        """
        开始生成 crud 代码，并直接写入到项目中，目前还未实现
        1. 生成 schemas 代码
        2. 生成 dal 代码
        3. 生成 params 代码
        4. 生成 views 代码
        :return:
        """
        schema = SchemaGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.schema_file_path,
            self.schemas_dir_path,
            self.base_class_name,
            self.schema_simple_out_class_name
        )
        schema.write_generate_code()

        dal = DalGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.dal_class_name,
            self.schema_simple_out_class_name
        )
        dal.write_generate_code()

        params = ParamsGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.params_dir_path,
            self.param_file_path,
            self.param_class_name
        )
        params.write_generate_code()

        view = ViewGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.base_class_name,
            self.schema_simple_out_class_name,
            self.dal_class_name,
            self.param_class_name
        )
        view.write_generate_code()
