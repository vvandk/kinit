#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据库 增删改查操作

# sqlalchemy 查询操作：https://segmentfault.com/a/1190000016767008
# sqlalchemy 关联查询：https://www.jianshu.com/p/dfad7c08c57a
# sqlalchemy 关联查询详细：https://blog.csdn.net/u012324798/article/details/103940527
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from core.crud import DalBase


class DictTypeDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DictTypeDal, self).__init__(db, models.VadminDictType, schemas.DictTypeSimpleOut)

    async def get_dicts_details(self, dict_types: List[str]) -> dict:
        """
        获取多个字典类型下的字典元素列表
        """
        data = {}
        for dict_type in dict_types:
            dict_data = await DictTypeDal(self.db).\
                get_data(dict_type=dict_type, return_none=True, options=[self.model.details])
            if not dict_data:
                data[dict_type] = []
                continue
            else:
                data[dict_type] = [schemas.DictDetailsSimpleOut.from_orm(i).dict() for i in dict_data.details]
        return data

    async def get_select_datas(self):
        """获取选择数据，全部数据"""
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        return [schemas.DictTypeSelectOut.from_orm(i).dict() for i in queryset.scalars().all()]


class DictDetailsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DictDetailsDal, self).__init__(db, models.VadminDictDetails, schemas.DictDetailsSimpleOut)
