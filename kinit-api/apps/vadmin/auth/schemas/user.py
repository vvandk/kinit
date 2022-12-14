#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : user.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import List, Optional
from pydantic import BaseModel, root_validator
from core.data_types import Telephone, DatetimeStr
from .role import RoleSimpleOut


class User(BaseModel):
    name: str
    telephone: Telephone
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    is_cancel: Optional[bool] = False
    gender: Optional[str] = "0"


class UserIn(User):
    role_ids: Optional[List[int]] = []
    password: Optional[str] = ""


class UserSimpleOut(User):
    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr

    is_reset_password: Optional[bool] = None
    last_login: Optional[DatetimeStr] = None
    last_ip: Optional[str] = None

    class Config:
        orm_mode = True


class UserOut(UserSimpleOut):
    roles: Optional[List[RoleSimpleOut]] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str
    telephone: Telephone
    nickname: Optional[str] = None
    gender: Optional[str] = "0"


class ResetPwd(BaseModel):
    password: str
    password_two: str

    @root_validator
    def check_passwords_match(cls, values):
        pw1, pw2 = values.get('password'), values.get('password_two')
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('两次密码不一致!')
        return values
