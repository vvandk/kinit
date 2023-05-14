#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023-02-15 20:03:49
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 帮助中心 - 增删改查

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.crud import DalBase
from . import models, schemas
from apps.vadmin.auth import models as vadminAuthModels


class IssueDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(IssueDal, self).__init__(db, models.VadminIssue, schemas.IssueSimpleOut)

    async def add_view_number(self, data_id: int):
        """
        更新常见问题查看次数+1
        """
        obj = await self.get_data(data_id)
        obj.view_number = obj.view_number + 1 if obj.view_number else 1
        await self.flush(obj)
        return True


class IssueCategoryDal(DalBase):

    def __init__(self, db: AsyncSession):
        key_models = {
            # 外键字段名，也可以自定义
            "create_user": {
                # 外键对应的orm模型
                "model": vadminAuthModels.VadminUser,
                # 如果对同一个模型只有一个外键关联时，下面这个 onclause 可以省略不写，一个以上时必须写，需要分清楚要查询的是哪个
                # 这里其实可以省略不写，但是为了演示这里写出来了
                "onclause": models.VadminIssueCategory.create_user_id == vadminAuthModels.VadminUser.id
            }
        }
        super(IssueCategoryDal, self).__init__(
            db,
            models.VadminIssueCategory,
            schemas.IssueCategorySimpleOut,
            key_models
        )

    async def test(self):
        """
        v_join_query 示例方法
        获取用户名称包含李 创建出的常见问题类别
        """
        v_join_query = {
            # 与 key_models 中定义的外键字段名定义的一样
            "create_user": {
                # 外键表字段名：查询值
                "name": ("like", "李")
            }
        }
        v_options = [joinedload(self.model.create_user)]
        datas = self.get_datas(limit=0, v_join_query=v_join_query, v_options=v_options)
