import inspect
import sys
from pathlib import Path
from typing import Type
from core.database import Base
from .generate_base import GenerateBase


class ViewGenerate(GenerateBase):

    def __init__(
            self,
            model: Type[Base],
            zh_name: str,
            en_name: str,
            schema_class_name: str,
            schema_simple_out_class_name: str,
            dal_class_name: str,
            param_class_name: str
    ):
        """
        初始化工作
        :param model: 提前定义好的 ORM 模型
        :param zh_name: 功能中文名称，主要用于描述、注释
        :param schema_class_name:
        :param schema_simple_out_class_name:
        :param dal_class_name:
        :param param_class_name:
        :param en_name: 功能英文名称，主要用于 schema、param 文件命名，以及它们的 class 命名，dal、url 命名，默认使用 model class
        en_name 例子：
            如果 en_name 由多个单词组成那么请使用 _ 下划线拼接
            在命名文件名称时，会执行使用 _ 下划线名称
            在命名 class 名称时，会将下划线名称转换为大驼峰命名（CamelCase）
            在命名 url 时，会将下划线转换为 /
        """
        self.model = model
        self.schema_class_name = schema_class_name
        self.schema_simple_out_class_name = schema_simple_out_class_name
        self.dal_class_name = dal_class_name
        self.param_class_name = param_class_name
        self.zh_name = zh_name
        self.en_name = en_name
        # model 文件的地址
        self.model_file_path = Path(inspect.getfile(sys.modules[model.__module__]))
        # model 文件 app 路径
        self.app_dir_path = self.model_file_path.parent.parent
        # view 文件地址
        self.view_file_path = self.app_dir_path / "views.py"

    def write_generate_code(self):
        """
        生成 view 文件，以及代码内容
        :return:
        """
        if self.view_file_path.exists():
            codes = self.file_code_split_module(self.view_file_path)
            if codes:
                print(f"==========view 文件已存在并已有代码内容，正在追加新代码============")
                if not codes[0]:
                    # 无文件注释则添加文件注释
                    codes[0] = self.generate_file_desc(self.view_file_path.name, "1.0", "视图层")
                codes[1] = self.merge_dictionaries(codes[1], self.get_base_module_config())
                codes[2] += self.get_base_code_content()
                code = ''
                code += codes[0]
                code += self.generate_modules_code(codes[1])
                if "app = APIRouter()" not in codes[2]:
                    code += "\n\napp = APIRouter()"
                code += codes[2]
                self.view_file_path.write_text(code, "utf-8")
                print(f"=================view 代码已创建完成=====================")
                return
        else:
            self.view_file_path.touch()
            code = self.generate_code()
            self.view_file_path.write_text(code, encoding="utf-8")
            print(f"===============view 代码创建完成==================")

    def generate_code(self) -> str:
        """
        生成代码
        :return:
        """
        code = self.generate_file_desc(self.view_file_path.name, "1.0", "路由，视图文件")
        code += self.generate_modules_code(self.get_base_module_config())
        code += "\n\napp = APIRouter()"
        code += self.get_base_code_content()

        return code.replace("\t", "    ")

    @staticmethod
    def get_base_module_config():
        """
        获取基础模块导入配置
        :return:
        """
        modules = {
            "sqlalchemy.ext.asyncio": ['AsyncSession'],
            "fastapi": ["APIRouter", "Depends"],
            ".": ["models", "schemas", "crud", "params"],
            "core.dependencies": ["IdList"],
            "apps.vadmin.auth.utils.current": ["AllUserAuth"],
            "utils.response": ["SuccessResponse"],
            "apps.vadmin.auth.utils.validation.auth": ["Auth"],
            "core.database": ["db_getter"],
        }
        return modules

    def get_base_code_content(self):
        """
        获取基础代码内容
        :return:
        """
        base_code = "\n\n\n###########################################################"
        base_code += f"\n#    {self.zh_name}"
        base_code += "\n###########################################################"

        router = self.en_name.replace("_", "/")

        base_code += f"\n@app.get(\"/{router}\", summary=\"获取{self.zh_name}列表\", tags=[\"{self.zh_name}\"])"
        base_code += f"\nasync def get_{self.en_name}_list(p: params.{self.param_class_name} = Depends(), auth: Auth = Depends(AllUserAuth())):"
        base_code += f"\n\tdatas, count = await crud.{self.dal_class_name}(auth.db).get_datas(**p.dict(), v_return_count=True)"
        base_code += f"\n\treturn SuccessResponse(datas, count=count)\n"

        base_code += f"\n\n@app.post(\"/{router}\", summary=\"创建{self.zh_name}\", tags=[\"{self.zh_name}\"])"
        base_code += f"\nasync def create_{self.en_name}(data: schemas.{self.schema_class_name}, auth: Auth = Depends(AllUserAuth())):"
        base_code += f"\n\treturn SuccessResponse(await crud.{self.dal_class_name}(auth.db).create_data(data=data))\n"

        base_code += f"\n\n@app.delete(\"/{router}\", summary=\"删除{self.zh_name}\", description=\"硬删除\", tags=[\"{self.zh_name}\"])"
        base_code += f"\nasync def delete_{self.en_name}_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):"
        base_code += f"\n\tawait crud.{self.dal_class_name}(auth.db).delete_datas(ids=ids.ids, v_soft=False)"
        base_code += f"\n\treturn SuccessResponse(\"删除成功\")\n"

        base_code += f"\n\n@app.put(\"/{router}" + "/{data_id}\"" + f", summary=\"更新{self.zh_name}\", tags=[\"{self.zh_name}\"])"
        base_code += f"\nasync def put_{self.en_name}(data_id: int, data: schemas.{self.schema_class_name}, auth: Auth = Depends(AllUserAuth())):"
        base_code += f"\n\treturn SuccessResponse(await crud.{self.dal_class_name}(auth.db).put_data(data_id, data))\n"

        base_code += f"\n\n@app.get(\"/{router}" + "/{data_id}\"" + f", summary=\"获取{self.zh_name}信息\", tags=[\"{self.zh_name}\"])"
        base_code += f"\nasync def get_{self.en_name}(data_id: int, db: AsyncSession = Depends(db_getter)):"
        base_code += f"\n\tschema = schemas.{self.schema_simple_out_class_name}"
        base_code += f"\n\treturn SuccessResponse(await crud.{self.dal_class_name}(db).get_data(data_id, v_schema=schema))\n"
        base_code += "\n"
        return base_code.replace("\t", "    ")
