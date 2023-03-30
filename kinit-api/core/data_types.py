#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/11/14 12:42 
# @File           : data_types.py
# @IDE            : PyCharm
# @desc           : 自定义数据类型

"""
自定义数据类型 - 官方文档：https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
"""

from .validator import *


class DatetimeStr(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return v
        return v.strftime("%Y-%m-%d %H:%M:%S")


class Telephone(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return vali_telephone(v)


class Email(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return vali_email(v)


class DateStr(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return v
        return v.strftime("%Y-%m-%d")
