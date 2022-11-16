#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : settings_tab.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from pydantic import BaseModel
from core.data_types import DatetimeStr


class SettingsTab(BaseModel):
    title: str
    classify: str
    tab_label: str
    tab_name: str
    hidden: bool


class SettingsTabSimpleOut(SettingsTab):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    class Config:
        orm_mode = True
