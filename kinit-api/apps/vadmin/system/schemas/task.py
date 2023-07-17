#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/25 15:08 
# @File           : task.py
# @IDE            : PyCharm
# @desc           : 简要说明

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr, ObjectIdStr


class Task(BaseModel):
    name: str
    group: str | None = None
    job_class: str
    exec_strategy: str
    expression: str
    is_active: bool | None = True  # 临时字段，不在表中创建
    remark: str | None = None
    start_date: DatetimeStr | None = None
    end_date: DatetimeStr | None = None


class TaskSimpleOut(Task):
    model_config = ConfigDict(from_attributes=True)

    id: ObjectIdStr = Field(..., alias='_id')
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
    last_run_datetime: DatetimeStr | None = None  # 临时字段，不在表中创建

