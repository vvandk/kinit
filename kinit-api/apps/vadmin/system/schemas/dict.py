#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : dict.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class DictType(BaseModel):
    dict_name: str
    dict_type: str
    disabled: bool | None = False
    remark: str | None = None


class DictTypeSimpleOut(DictType):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class DictTypeOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label: str = Field(alias='dict_name')
    value: int = Field(alias='id')
    disabled: bool


class DictDetails(BaseModel):
    label: str
    value: str
    disabled: bool | None = False
    is_default: bool | None = False
    remark: str | None = None
    order: int | None = None
    dict_type_id: int


class DictDetailsSimpleOut(DictDetails):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

