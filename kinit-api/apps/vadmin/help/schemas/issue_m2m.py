#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/2/17 15:18 
# @File           : issue_m2m.py.py
# @IDE            : PyCharm
# @desc           : 简要说明

from typing import Optional, List
from pydantic import BaseModel, Field
from core.data_types import DatetimeStr
from .issue import IssueSimpleOut


class IssueCategoryPlatformOut(BaseModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    is_active: Optional[bool] = None
    create_user_id: Optional[int] = None

    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr

    issues: Optional[List[IssueSimpleOut]] = None

    class Config:
        orm_mode = True

