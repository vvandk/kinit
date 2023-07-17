#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/7/16 12:42
# @File           : data_types.py
# @IDE            : PyCharm
# @desc           : 自定义数据类型

"""
自定义数据类型 - 官方文档：https://docs.pydantic.dev/dev-v2/usage/types/custom/#adding-validation-and-serialization
"""
import datetime
from typing import Annotated, Any

from bson import ObjectId
from pydantic import AfterValidator, PlainSerializer, WithJsonSchema
from .validator import *


def DatetimeStrVali(value: str | datetime.datetime | int | float | dict):
    """
    日期时间字符串验证
    如果我传入的是字符串，那么直接返回，如果我传入的是一个日期类型，那么会转为字符串格式后返回
    因为在 pydantic 2.0 中是支持 int 或 float 自动转换类型的，所以我这里添加进去，但是在处理时会使这两种类型报错

    官方文档：https://docs.pydantic.dev/dev-v2/usage/types/datetime/
    """
    if isinstance(value, str):
        pattern = "%Y-%m-%d %H:%M:%S"
        try:
            datetime.datetime.strptime(value, pattern)
            return value
        except ValueError:
            pass
    elif isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, dict):
        # 用于处理 mongodb 日期时间数据类型
        date_str = value.get("$date")
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        # 将字符串转换为datetime.datetime类型
        datetime_obj = datetime.datetime.strptime(date_str, date_format)
        # 将datetime.datetime对象转换为指定的字符串格式
        return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    raise ValueError("无效的日期时间或字符串数据")


# 实现自定义一个日期时间字符串的数据类型
DatetimeStr = Annotated[
    str | datetime.datetime | int | float | dict,
    AfterValidator(DatetimeStrVali),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


# 实现自定义一个手机号类型
Telephone = Annotated[
    str,
    AfterValidator(lambda x: vali_telephone(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


# 实现自定义一个邮箱类型
Email = Annotated[
    str,
    AfterValidator(lambda x: vali_email(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


def DateStrVali(value: str | datetime.date | int | float):
    """
    日期字符串验证
    如果我传入的是字符串，那么直接返回，如果我传入的是一个日期类型，那么会转为字符串格式后返回
    因为在 pydantic 2.0 中是支持 int 或 float 自动转换类型的，所以我这里添加进去，但是在处理时会使这两种类型报错

    官方文档：https://docs.pydantic.dev/dev-v2/usage/types/datetime/
    """
    if isinstance(value, str):
        pattern = "%Y-%m-%d"
        try:
            datetime.datetime.strptime(value, pattern)
            return value
        except ValueError:
            pass
    elif isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    raise ValueError("无效的日期时间或字符串数据")


# 实现自定义一个日期字符串的数据类型
DateStr = Annotated[
    str | datetime.date | int | float,
    AfterValidator(DateStrVali),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


def ObjectIdStrVali(value: str | dict | ObjectId):
    """
    官方文档：https://docs.pydantic.dev/dev-v2/usage/types/datetime/
    """
    if isinstance(value, str):
        return value
    elif isinstance(value, dict):
        return value.get("$oid")
    elif isinstance(value, ObjectId):
        return str(value)
    raise ValueError("无效的 ObjectId 数据类型")


ObjectIdStr = Annotated[
    Any,  # 这里不能直接使用 any，需要使用 typing.Any
    AfterValidator(ObjectIdStrVali),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]
