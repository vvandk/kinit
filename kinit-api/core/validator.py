#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : validator.py
# @IDE            : PyCharm
# @desc           : pydantic 模型重用验证器

"""
官方文档：https://pydantic-docs.helpmanual.io/usage/validators/#reuse-validators
"""

import re


def vali_telephone(value: str) -> str:
    """
    手机号验证器
    :param value: 手机号
    :return: 手机号
    """
    if not value or len(value) != 11 or not value.isdigit():
        raise ValueError("请输入正确手机号")

    REGEX_TELEPHONE = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'

    if not re.match(REGEX_TELEPHONE, value):
        raise ValueError("请输入正确手机号")

    return value


class ValiDatetime(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return v.strftime("%Y-%m-%d %H:%M:%S")

