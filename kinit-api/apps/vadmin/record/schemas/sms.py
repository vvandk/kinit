#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/3/21 17:54 
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 简要说明


from typing import Optional, List
from pydantic import BaseModel
from core.data_types import DatetimeStr


class SMSSendRecord(BaseModel):
    telephone: str
    status: bool = True
    user_id: Optional[int] = None
    content: Optional[str] = None
    desc: Optional[str] = None
    scene: Optional[str] = None


class SMSSendRecordSimpleOut(SMSSendRecord):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    class Config:
        orm_mode = True
