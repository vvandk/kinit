#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : operation.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import Optional, List
from pydantic import BaseModel


class OpertionRecord(BaseModel):
    telephone: Optional[str] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    status_code: Optional[int] = None
    request_ip: Optional[str] = None
    request_method: Optional[str] = None
    api_path: Optional[str] = None
    system: Optional[str] = None
    browser: Optional[str] = None
    summary: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    process_time: Optional[str] = None
    params: Optional[str] = None
    create_datetime: Optional[str] = None


class OpertionRecordSimpleOut(OpertionRecord):

    class Config:
        orm_mode = True
