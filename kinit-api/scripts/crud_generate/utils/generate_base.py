import datetime
import re
from pathlib import Path


class GenerateBase:

    @staticmethod
    def camel_to_snake(name: str) -> str:
        """
        将大驼峰命名（CamelCase）转换为下划线命名（snake_case）
        在大写字母前添加一个空格，然后将字符串分割并用下划线拼接
        :param name: 大驼峰命名（CamelCase）
        :return:
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def snake_to_camel(name: str) -> str:
        """
        将下划线命名（snake_case）转换为大驼峰命名（CamelCase）
        根据下划线分割，然后将字符串转为第一个字符大写后拼接
        :param name: 下划线命名（snake_case）
        :return:
        """
        # 按下划线分割字符串
        words = name.split('_')
        # 将每个单词的首字母大写，然后拼接
        return ''.join(word.capitalize() for word in words)

    @staticmethod
    def generate_file_desc(filename: str, version: str = '1.0', desc: str = '') -> str:
        """
        生成文件注释
        :param filename:
        :param version:
        :param desc:
        :return:
        """
        code = '#!/usr/bin/python\n# -*- coding: utf-8 -*-'
        code += f"\n# @version        : {version}"
        code += f"\n# @Create Time    : {datetime.datetime.now().strftime('%Y/%m/%d %H:%M')}"
        code += f"\n# @File           : {filename}"
        code += f"\n# @IDE            : PyCharm"
        code += f"\n# @desc           : {desc}"
        code += f"\n"
        return code

    @staticmethod
    def generate_modules_code(modules: dict[str, list]) -> str:
        """
        生成模块导入代码
        :param modules: 导入得模块
        :return:
        """
        code = "\n"
        args = modules.pop("args", [])
        for k, v in modules.items():
            code += f"from {k} import {', '.join(v)}\n"
        if args:
            code += f"import {', '.join(args)}\n"
        return code

    @staticmethod
    def update_init_file(init_file: Path, code: str):
        """
        __init__ 文件添加导入内容
        :param init_file:
        :param code:
        :return:
        """
        content = init_file.read_text()
        if content and code in content:
            return
        if content:
            if content.endswith("\n"):
                with init_file.open("a+", encoding="utf-8") as f:
                    f.write(f"{code}\n")
            else:
                with init_file.open("a+", encoding="utf-8") as f:
                    f.write(f"\n{code}\n")
        else:
            init_file.write_text(f"{code}\n", encoding="utf-8")

    @staticmethod
    def module_code_to_dict(code: str) -> dict:
        """
        将 from import 语句代码转为 dict 格式
        :param code:
        :return:
        """
        # 分解代码为单行
        lines = code.strip().split('\n')

        # 初始化字典
        modules = {}

        # 遍历每行代码
        for line in lines:
            # 处理 'from ... import ...' 类型的导入
            if line.startswith('from'):
                parts = line.split(' import ')
                module = parts[0][5:]  # 移除 'from ' 并获取模块路径
                imports = parts[1].split(',')  # 使用逗号分割导入项
                imports = [item.strip() for item in imports]  # 移除多余空格
                if module in modules:
                    modules[module].extend(imports)
                else:
                    modules[module] = imports

            # 处理 'import ...' 类型的导入
            elif line.startswith('import'):
                imports = line.split('import ')[1]
                # 分割多个导入项
                imports = imports.split(', ')
                for imp in imports:
                    # 处理直接导入的模块
                    modules.setdefault('args', []).append(imp)
        return modules

    @classmethod
    def file_code_split_module(cls, file: Path) -> list:
        """
        文件代码内容拆分，分为以下三部分
        1. 文件开头的注释。
        2. 全局层面的from import语句。该代码格式会被转换为 dict 格式
        3. 其他代码内容。
        :param file:
        :return:
        """
        content = file.read_text(encoding="utf-8")
        if not content:
            return []
        lines = content.split('\n')
        part1 = []  # 文件开头注释
        part2 = []  # from import 语句
        part3 = []  # 其他代码内容

        # 标记是否已超过注释部分
        past_comments = False

        for line in lines:
            # 检查是否为注释行
            if line.startswith("#") and not past_comments:
                part1.append(line)
            else:
                # 标记已超过注释部分
                past_comments = True
                # 检查是否为 from import 语句
                if line.startswith("from ") or line.startswith("import "):
                    part2.append(line)
                else:
                    part3.append(line)

        part2 = cls.module_code_to_dict('\n'.join(part2))

        return ['\n'.join(part1), part2, '\n'.join(part3)]

    @staticmethod
    def merge_dictionaries(dict1, dict2):
        """
        合并两个键为字符串、值为列表的字典
        :param dict1:
        :param dict2:
        :return:
        """
        # 初始化结果字典
        merged_dict = {}

        # 合并两个字典中的键值对
        for key in set(dict1) | set(dict2):  # 获取两个字典的键的并集
            merged_dict[key] = list(set(dict1.get(key, []) + dict2.get(key, [])))

        return merged_dict


if __name__ == '__main__':
    _modules = {
        "sqlalchemy.ext.asyncio": ['AsyncSession'],
        "core.crud": ["DalBase"],
        ".": ["models", "schemas"],
        "args": ["test", "test1"]
    }
    print(GenerateBase.generate_modules_code(_modules))
