#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023-02-15 20:03:49
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 帮助中心 - 增删改查

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class IssueDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(IssueDal, self).__init__(db, models.VadminIssue, schemas.IssueSimpleOut)

    async def add_view_number(self, data_id: int) -> None:
        """
        更新常见问题查看次数+1
        """
        obj: models.VadminIssue = await self.get_data(data_id)
        obj.view_number = obj.view_number + 1 if obj.view_number else 1
        await self.flush(obj)


class IssueCategoryDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(IssueCategoryDal, self).__init__(db, models.VadminIssueCategory, schemas.IssueCategorySimpleOut)
