#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/8/25 13:15
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 简要说明

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class ImagesDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ImagesDal, self).__init__(db, models.VadminImages, schemas.ImagesSimpleOut)
