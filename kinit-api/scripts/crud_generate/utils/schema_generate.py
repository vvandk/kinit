# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/1/12 17:28
# @File           : schema_generate.py
# @IDE            : PyCharm
# @desc           : schema 代码生成


import sys
from typing import Type
import inspect
from sqlalchemy import inspect as model_inspect
from pathlib import Path
from core.database import Base
from scripts.crud_generate.utils.schema import SchemaField
from sqlalchemy.sql.schema import Column as ColumnType
from scripts.crud_generate.utils.generate_base import GenerateBase


class SchemaGenerate(GenerateBase):

    BASE_FIELDS = ["id", "create_datetime", "update_datetime", "delete_datetime", "is_delete"]

    def __init__(
            self,
            model: Type[Base],
            zh_name: str,
            en_name: str,
            schema_file_path: Path,
            schemas_dir_path: Path,
            base_class_name: str,
            schema_simple_out_class_name: str
    ):
        """
        初始化工作
        :param model: 提前定义好的 ORM 模型
        :param zh_name: 功能中文名称，主要用于描述、注释
        :param schema_file_path:
        :param en_name: 功能英文名称，主要用于 schema、param 文件命名，以及它们的 class 命名，dal、url 命名，默认使用 model class
        en_name 例子：
            如果 en_name 由多个单词组成那么请使用 _ 下划线拼接
            在命名文件名称时，会执行使用 _ 下划线名称
            在命名 class 名称时，会将下划线名称转换为大驼峰命名（CamelCase）
            在命名 url 时，会将下划线转换为 /
        :param base_class_name:
        :param schema_simple_out_class_name:
        """
        self.model = model
        self.base_class_name = base_class_name
        self.schema_simple_out_class_name = schema_simple_out_class_name
        self.zh_name = zh_name
        # model 文件的地址
        self.model_file_path = Path(inspect.getfile(sys.modules[model.__module__]))
        # model 文件 app 路径
        self.app_dir_path = self.model_file_path.parent.parent
        self.en_name = en_name
        self.schema_file_path = schema_file_path
        self.schemas_dir_path = schemas_dir_path
        self.schema_init_file_path = self.schemas_dir_path / "__init__.py"

    def write_generate_code(self):
        """
        生成 schema 文件，以及代码内容
        :return:
        """
        self.schema_file_path.parent.mkdir(parents=True, exist_ok=True)
        if self.schema_file_path.exists():
            # 存在则直接删除，重新创建写入
            self.schema_file_path.unlink()
        self.schema_file_path.touch()
        self.schema_init_file_path.touch()

        code = self.generate_code()
        self.schema_file_path.write_text(code, "utf-8")

        init_code = self.generate_init_code()
        self.update_init_file(self.schema_init_file_path, init_code)
        print(f"===========================schema 代码创建完成=================================")

    def generate_init_code(self):
        """
        生成 __init__ 文件导入代码
        todo 如果导入的类已经存在，则应该返回空
        :return:
        """
        init_code = f"from .{self.en_name} import {self.base_class_name}, {self.schema_simple_out_class_name}"
        return init_code

    def generate_code(self) -> str:
        """
        生成 schema 代码内容
        :return:
        """
        fields = []
        mapper = model_inspect(self.model)
        for attr_name, column_property in mapper.column_attrs.items():
            if attr_name in self.BASE_FIELDS:
                continue
            # 假设它是单列属性
            column: ColumnType = column_property.columns[0]
            item = SchemaField(
                name=attr_name,
                field_type=column.type.python_type.__name__,
                nullable=column.nullable,
                default=column.default.__dict__.get("arg", None) if column.default else None,
                title=column.comment,
                max_length=column.type.__dict__.get("length", None)
            )
            fields.append(item)

        code = self.generate_file_desc(self.schema_file_path.name, "1.0", "pydantic 模型，用于数据库序列化操作")

        modules = {
            "pydantic": ['BaseModel', "Field", "ConfigDict"],
            "core.data_types": ['DatetimeStr'],
        }
        code += self.generate_modules_code(modules)

        base_schema_code = f"\n\nclass {self.base_class_name}(BaseModel):"
        for item in fields:
            field = f"\n\t{item.name}: {item.field_type} {'| None ' if item.nullable else ''}"
            default = None
            if item.default is not None:
                if item.field_type == "str":
                    default = f"\"{item.default}\""
                else:
                    default = item.default
            elif default is None and not item.nullable:
                default = "..."

            field += f"= Field({default}, title=\"{item.title}\")"
            base_schema_code += field
        base_schema_code += "\n"
        code += base_schema_code

        base_out_schema_code = f"\n\nclass {self.schema_simple_out_class_name}({self.base_class_name}):"
        base_out_schema_code += "\n\tmodel_config = ConfigDict(from_attributes=True)\n"
        base_out_schema_code += "\n\tid: int = Field(..., title=\"编号\")"
        base_out_schema_code += "\n\tcreate_datetime: DatetimeStr = Field(..., title=\"创建时间\")"
        base_out_schema_code += "\n\tupdate_datetime: DatetimeStr = Field(..., title=\"更新时间\")"
        base_out_schema_code += "\n"
        code += base_out_schema_code
        return code.replace("\t", "    ")
