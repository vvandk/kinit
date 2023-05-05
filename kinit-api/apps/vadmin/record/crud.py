#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据库 增删改查操作
import random
from typing import List

# sqlalchemy 查询操作：https://segmentfault.com/a/1190000016767008
# sqlalchemy 关联查询：https://www.jianshu.com/p/dfad7c08c57a
# sqlalchemy 关联查询详细：https://blog.csdn.net/u012324798/article/details/103940527
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from core.crud import DalBase


class LoginRecordDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(LoginRecordDal, self).__init__(db, models.VadminLoginRecord, schemas.LoginRecordSimpleOut)

    async def get_user_distribute(self) -> List[dict]:
        """
        获取用户登录分布情况
        高德经纬度查询：https://lbs.amap.com/tools/picker

        {
            name: '北京',
            center: [116.407394, 39.904211],
            total: 20
        }

        :return: List[dict]
        """
        result = [{
                    "name": '北京',
                    "center": [116.407394, 39.904211],
                },
                {
                    "name": '重庆',
                    "center": [106.551643, 29.562849],
                },
                {
                    "name": '郑州',
                    "center": [113.778584, 34.759197],
                },
                {
                    "name": '南京',
                    "center": [118.796624, 32.059344],
                },
                {
                    "name": '武汉',
                    "center": [114.304569, 30.593354],
                },
                {
                    "name": '乌鲁木齐',
                    "center": [87.616824, 43.825377],
                },
                {
                    "name": '新乡',
                    "center": [113.92679, 35.303589],
                }]
        for data in result:
            assert isinstance(data, dict)
            data["total"] = random.randint(2, 80)
        return result


class SMSSendRecordDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SMSSendRecordDal, self).__init__(db, models.VadminSMSSendRecord, schemas.SMSSendRecordSimpleOut)
