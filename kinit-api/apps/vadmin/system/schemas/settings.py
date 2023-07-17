#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : settings.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr


class Settings(BaseModel):
    config_label: str | None = None
    config_key: str
    config_value: str | None = None
    remark: str | None = None
    disabled: bool | None = None
    tab_id: int


class SettingsSimpleOut(Settings):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

