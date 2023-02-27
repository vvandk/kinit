#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : issue_category.py
# @IDE            : PyCharm
# @desc           : 常见问题类别


from typing import Optional
from pydantic import BaseModel, Field
from core.data_types import DatetimeStr
from apps.vadmin.auth.schemas import UserSimpleOut


class IssueCategory(BaseModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    is_active: Optional[bool] = None

    user_id: Optional[int] = None


class IssueCategorySimpleOut(IssueCategory):
    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr

    class Config:
        orm_mode = True


class IssueCategoryListOut(IssueCategorySimpleOut):
    user: UserSimpleOut

    class Config:
        orm_mode = True


class IssueCategoryOptionsOut(BaseModel):
    label: str = Field(alias='name')
    value: int = Field(alias='id')

    class Config:
        orm_mode = True
