import inspect
import sys
from pathlib import Path
from typing import Type
from core.database import Base
from .generate_base import GenerateBase


class DalGenerate(GenerateBase):

    def __init__(
            self,
            model: Type[Base],
            zh_name: str,
            en_name: str,
            dal_class_name: str,
            schema_simple_out_class_name: str
    ):
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
        :param dal_class_name:
        :param schema_simple_out_class_name:
        """
        self.model = model
        self.dal_class_name = dal_class_name
        self.schema_simple_out_class_name = schema_simple_out_class_name
        self.zh_name = zh_name
        self.en_name = en_name
        # model 文件的地址
        self.model_file_path = Path(inspect.getfile(sys.modules[model.__module__]))
        # model 文件 app 路径
        self.app_dir_path = self.model_file_path.parent.parent
        # crud 文件地址
        self.crud_file_path = self.app_dir_path / "crud.py"

    def write_generate_code(self):
        """
        生成 crud 文件，以及代码内容
        :return:
        """
        if self.crud_file_path.exists():
            codes = self.file_code_split_module(self.crud_file_path)
            if codes:
                print(f"==========dal 文件已存在并已有代码内容，正在追加新代码============")
                if not codes[0]:
                    # 无文件注释则添加文件注释
                    codes[0] = self.generate_file_desc(self.crud_file_path.name, "1.0", "数据访问层")
                codes[1] = self.merge_dictionaries(codes[1], self.get_base_module_config())
                codes[2] += self.get_base_code_content()
                code = ''
                code += codes[0]
                code += self.generate_modules_code(codes[1])
                code += codes[2]
                self.crud_file_path.write_text(code, "utf-8")
                print(f"=================dal 代码已创建完成=======================")
                return
        self.crud_file_path.touch()
        code = self.generate_code()
        self.crud_file_path.write_text(code, "utf-8")
        print(f"===========================dal 代码创建完成=================================")

    def generate_code(self):
        """
        代码生成
        :return:
        """
        code = self.generate_file_desc(self.crud_file_path.name, "1.0", "数据访问层")
        code += self.generate_modules_code(self.get_base_module_config())
        code += self.get_base_code_content()
        return code

    @staticmethod
    def get_base_module_config():
        """
        获取基础模块导入配置
        :return:
        """
        modules = {
            "sqlalchemy.ext.asyncio": ['AsyncSession'],
            "core.crud": ["DalBase"],
            ".": ["models", "schemas"],
        }
        return modules

    def get_base_code_content(self):
        """
        获取基础代码内容
        :return:
        """
        base_code = f"\n\nclass {self.dal_class_name}(DalBase):\n"
        base_code += "\n\tdef __init__(self, db: AsyncSession):"
        base_code += f"\n\t\tsuper({self.dal_class_name}, self).__init__()"
        base_code += f"\n\t\tself.db = db"
        base_code += f"\n\t\tself.model = models.{self.model.__name__}"
        base_code += f"\n\t\tself.schema = schemas.{self.schema_simple_out_class_name}"
        base_code += "\n"
        return base_code.replace("\t", "    ")

