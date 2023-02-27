#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : issue.py
# @IDE            : PyCharm
# @desc           : 常见问题

from typing import Optional
from pydantic import BaseModel
from core.data_types import DatetimeStr
from apps.vadmin.auth.schemas import UserSimpleOut
from .issue_category import IssueCategorySimpleOut


class Issue(BaseModel):
    category_id: Optional[int] = None
    user_id: Optional[int] = None

    title: Optional[str] = None
    content: Optional[str] = None
    view_number: Optional[int] = None
    is_active: Optional[bool] = None


class IssueSimpleOut(Issue):
    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr

    class Config:
        orm_mode = True


class IssueListOut(IssueSimpleOut):
    user: UserSimpleOut
    category: IssueCategorySimpleOut

    class Config:
        orm_mode = True
