#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : settings.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import Optional, List
from pydantic import BaseModel
from core.data_types import DatetimeStr


class Settings(BaseModel):
    config_label: Optional[str] = None
    config_key: str
    config_value: Optional[str] = None
    remark: Optional[str] = None
    disabled: Optional[bool] = None
    tab_id: int


class SettingsSimpleOut(Settings):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    class Config:
        orm_mode = True
