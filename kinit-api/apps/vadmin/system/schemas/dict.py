#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : dict.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import Optional, List
from pydantic import BaseModel
from core.validator import ValiDatetime


class DictType(BaseModel):
    dict_name: str
    dict_type: str
    disabled: Optional[bool] = False
    remark: Optional[str] = None


class DictTypeSimpleOut(DictType):
    id: int
    create_datetime: ValiDatetime
    update_datetime: ValiDatetime

    class Config:
        orm_mode = True


class DictTypeSelectOut(BaseModel):
    id: int
    dict_name: str
    disabled: bool

    class Config:
        orm_mode = True


class DictDetails(BaseModel):
    label: str
    value: str
    disabled: Optional[bool] = False
    is_default: Optional[bool] = False
    remark: Optional[str] = None
    order: Optional[int] = None
    dict_type_id: int


class DictDetailsSimpleOut(DictDetails):
    id: int
    create_datetime: ValiDatetime
    update_datetime: ValiDatetime

    class Config:
        orm_mode = True
