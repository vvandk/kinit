#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : operation.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr


class OperationRecord(BaseModel):
    telephone: str | None = None
    user_id: int | None = None
    user_name: str | None = None
    status_code: int | None = None
    client_ip: str | None = None
    request_method: str | None = None
    api_path: str | None = None
    system: str | None = None
    browser: str | None = None
    summary: str | None = None
    route_name: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    process_time: float | None = None
    params: str | None = None


class OperationRecordSimpleOut(OperationRecord):
    model_config = ConfigDict(from_attributes=True)

    create_datetime: DatetimeStr
