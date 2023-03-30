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
from core.data_types import Telephone, DatetimeStr, Email
from .role import RoleSimpleOut


class User(BaseModel):
    name: Optional[str] = None
    telephone: Telephone
    email: Optional[Email] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    is_staff: Optional[bool] = False
    gender: Optional[str] = "0"
    is_wx_server_openid: Optional[bool] = False


class UserIn(User):
    """
    创建用户
    """
    role_ids: Optional[List[int]] = []
    password: Optional[str] = ""


class UserUpdateBaseInfo(BaseModel):
    """
    更新用户基本信息
    """
    name: str
    telephone: Telephone
    email: Optional[Email] = None
    nickname: Optional[str] = None
    gender: Optional[str] = "0"


class UserUpdate(User):
    """
    更新用户详细信息
    """
    name: Optional[str] = None
    telephone: Telephone
    email: Optional[Email] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    is_staff: Optional[bool] = False
    gender: Optional[str] = "0"
    role_ids: Optional[List[int]] = []


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


class ResetPwd(BaseModel):
    password: str
    password_two: str

    @root_validator
    def check_passwords_match(cls, values):
        pw1, pw2 = values.get('password'), values.get('password_two')
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('两次密码不一致!')
        return values
