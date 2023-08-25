#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/8/25 14:49
# @File           : images.py
# @IDE            : PyCharm
# @desc           : 简要说明


from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr
from apps.vadmin.auth.schemas import UserSimpleOut


class Images(BaseModel):
    filename: str
    image_url: str

    create_user_id: int


class ImagesSimpleOut(Images):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class ImagesOut(ImagesSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    create_user: UserSimpleOut
