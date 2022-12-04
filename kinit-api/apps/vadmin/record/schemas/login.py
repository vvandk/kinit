#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : login.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import Optional
from pydantic import BaseModel
from core.data_types import DatetimeStr


class LoginRecord(BaseModel):
    telephone: str
    status: bool
    ip: Optional[str] = None
    address: Optional[str] = None
    browser: Optional[str] = None
    system: Optional[str] = None
    response: Optional[str] = None
    request: Optional[str] = None
    postal_code: Optional[str] = None
    area_code: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    operator: Optional[str] = None
    platform: Optional[str] = None
    login_method: Optional[str] = None


class LoginRecordSimpleOut(LoginRecord):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    class Config:
        orm_mode = True
