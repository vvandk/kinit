#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : operation.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import Optional, List
from pydantic import BaseModel
from core.data_types import DatetimeStr, ObjectIdStr


class OperationRecord(BaseModel):
    telephone: Optional[str] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    status_code: Optional[int] = None
    client_ip: Optional[str] = None
    request_method: Optional[str] = None
    api_path: Optional[str] = None
    system: Optional[str] = None
    browser: Optional[str] = None
    summary: Optional[str] = None
    route_name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    process_time: Optional[str] = None
    params: Optional[str] = None


class OperationRecordSimpleOut(OperationRecord):
    create_datetime: DatetimeStr

    class Config:
        orm_mode = True
