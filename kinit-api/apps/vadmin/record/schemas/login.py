#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : login.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr


class LoginRecord(BaseModel):
    telephone: str
    status: bool
    ip: str | None = None
    address: str | None = None
    browser: str | None = None
    system: str | None = None
    response: str | None = None
    request: str | None = None
    postal_code: str | None = None
    area_code: str | None = None
    country: str | None = None
    province: str | None = None
    city: str | None = None
    county: str | None = None
    operator: str | None = None
    platform: str | None = None
    login_method: str | None = None


class LoginRecordSimpleOut(LoginRecord):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
