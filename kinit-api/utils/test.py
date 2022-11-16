#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/11/16 8:55 
# @File           : test.py
# @IDE            : PyCharm
# @desc           : 测试文件
from enum import Enum


class Scene(Enum):
    login = "template_code_1"
    reset_password = "template_code_2"


if __name__ == '__main__':
    print(Scene.login.value)