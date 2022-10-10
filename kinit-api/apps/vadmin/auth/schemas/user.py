#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : user.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import List, Optional
from pydantic import BaseModel, validator
from core.validator import vali_telephone, ValiDatetime
from .role import RoleSimpleOut


class User(BaseModel):
    name: str
    telephone: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    is_cancel: Optional[bool] = False
    gender: Optional[str] = "0"

    # validators
    _normalize_telephone = validator('telephone', allow_reuse=True)(vali_telephone)


class UserIn(User):
    role_ids: Optional[List[int]] = []
    password: Optional[str] = ""


class UserSimpleOut(User):
    id: int
    update_datetime: ValiDatetime
    create_datetime: ValiDatetime

    class Config:
        orm_mode = True


class UserOut(UserSimpleOut):
    roles: Optional[List[RoleSimpleOut]] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str
    nickname: Optional[str] = None
    gender: Optional[str] = "0"


class ResetPwd(BaseModel):
    password: str
    password_two: str
