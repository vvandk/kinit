#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/25 15:08 
# @File           : task.py
# @IDE            : PyCharm
# @desc           : 简要说明

from typing import Optional
from pydantic import BaseModel, Field
from core.data_types import DatetimeStr, ObjectIdStr


class Task(BaseModel):
    name: str
    group: Optional[str] = None
    job_class: str
    exec_strategy: str
    expression: str
    is_active: Optional[bool] = True  # 临时字段，不在表中创建
    remark: Optional[str] = None
    start_date: Optional[DatetimeStr] = None
    end_date: Optional[DatetimeStr] = None


class TaskSimpleOut(Task):
    id: ObjectIdStr = Field(..., alias='_id')
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
    last_run_datetime: Optional[DatetimeStr] = None # 临时字段，不在表中创建

    class Config:
        orm_mode = True
