#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/12/9 15:27 
# @File           : main.py
# @IDE            : PyCharm
# @desc           : 简要说明
import datetime
import os.path

from application.settings import BASE_DIR


class CreateApp:

    APPS_ROOT = os.path.join(BASE_DIR, "apps")
    SCRIPT_DIR = os.path.join(BASE_DIR, 'scripts', 'create_app')

    def __init__(self, path: str):
        """
        :param path: app 路径，根目录为apps，填写apps后面路径即可，例子：vadmin/auth
        """
        self.app_path = os.path.join(self.APPS_ROOT, path)
        self.path = path

    def run(self):
        """
        自动创建初始化 APP 结构，如何该路径已经存在，则不执行
        """
        if self.exist(self.app_path):
            print(f"{self.app_path} 已经存在，无法自动创建，请删除后，重新执行。")
            return False
        print("开始生成 App 目录：", self.path)
        path = []
        for item in self.path.split("/"):
            path.append(item)
            self.create_pag(os.path.join(self.APPS_ROOT, *path))
        self.create_pag(os.path.join(self.app_path, "models"))
        self.create_pag(os.path.join(self.app_path, "params"))
        self.create_pag(os.path.join(self.app_path, "schemas"))
        self.generate_file("views.py")
        self.generate_file("crud.py")
        print("App 目录生成结束", self.app_path)

    def create_pag(self, path: str) -> None:
        """
        创建 python 包

        :param path: 绝对路径
        """
        if self.exist(path):
            return
        os.makedirs(path)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = {
            "create_datetime": now,
            "filename": "__init__.py",
            "desc": "初始化文件"
        }
        self.create_file(os.path.join(path, "__init__.py"), "init.py", **params)

    def generate_file(self, name: str) -> None:
        """
        创建文件
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = {
            "create_datetime": now,
        }
        self.create_file(os.path.join(self.app_path, name), name, **params)

    def create_file(self, filepath: str, name: str, **kwargs):
        """
        创建文件
        """
        with open(filepath, "w", encoding="utf-8") as f:
            content = self.__get_template(name)
            f.write(content.format(**kwargs))

    @classmethod
    def exist(cls, path) -> bool:
        """
        判断路径是否已经存在
        """
        return os.path.exists(path)

    def __get_template(self, name: str) -> str:
        """
        获取模板内容
        """
        template = open(os.path.join(self.SCRIPT_DIR, "template", name), 'r')
        content = template.read()
        template.close()
        return content

