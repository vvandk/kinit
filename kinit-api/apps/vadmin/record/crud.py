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
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from core.crud import DalBase


class LoginRecordDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(LoginRecordDal, self).__init__(db, models.VadminLoginRecord, schemas.LoginRecordSimpleOut)


class SMSSendRecordDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(SMSSendRecordDal, self).__init__(db, models.VadminSMSSendRecord, schemas.SMSSendRecordSimpleOut)
