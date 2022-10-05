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

    class Config:
        # 示例参数值，会默认显示在接口文档中，example为固定写法
        schema_extra = {
            "example": {
                "dict_name": "用户性别",
                "dict_type": "sys_user_sex",
                "disabled": False,
                "remark": "性别选择"
            }
        }


class DictTypeSimpleOut(DictType):
    id: int
    create_datetime: ValiDatetime
    update_datetime: ValiDatetime

    class Config:
        orm_mode = True


class DictDetails(BaseModel):
    label: str
    value: str
    disabled: Optional[bool] = False
    is_default: Optional[bool] = False
    remark: Optional[str] = None
    order: Optional[str] = None
    dict_data: int


class DictDetailsSimpleOut(DictDetails):
    id: int
    create_datetime: ValiDatetime
    update_datetime: ValiDatetime

    class Config:
        orm_mode = True
