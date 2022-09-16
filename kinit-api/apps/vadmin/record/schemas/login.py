#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : login.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import Optional, List
from pydantic import BaseModel
from core.validator import ValiDatetime


class LoginRecord(BaseModel):
    telephone: str
    status: bool
    ip: Optional[str] = None
    address: Optional[str] = None
    browser: Optional[str] = None
    system: Optional[str] = None
    response: Optional[str] = None


class LoginRecordSimpleOut(LoginRecord):
    id: int
    create_datetime: ValiDatetime
    update_datetime: ValiDatetime

    class Config:
        orm_mode = True
