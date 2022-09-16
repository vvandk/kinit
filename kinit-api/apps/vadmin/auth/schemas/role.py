#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : role.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import Optional, List
from pydantic import BaseModel
from core.validator import ValiDatetime
from .menu import MenuSimpleOut


class Role(BaseModel):
    name: str
    is_active: bool = True
    index: Optional[int] = None
    desc: Optional[str] = None
    role_key: str
    is_admin: bool = False


class RoleSimpleOut(Role):
    id: int
    create_datetime: ValiDatetime
    update_datetime: ValiDatetime

    class Config:
        orm_mode = True


class RoleOut(RoleSimpleOut):
    menus: Optional[List[MenuSimpleOut]] = []

    class Config:
        orm_mode = True


class RoleIn(Role):
    menus: Optional[List[int]] = []


class RoleSelectOut(BaseModel):
    id: int
    name: str
    is_active: bool
    role_key: str

    class Config:
        orm_mode = True
