#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/3/21 11:03
# @File           : cache.py
# @IDE            : PyCharm
# @desc           : 保存缓存


from core.database import db_getter
from apps.vadmin.system.crud import SettingsTabDal
import json
from aioredis.client import Redis


async def cache_aliyun_settings(rd: Redis):
    """
    缓存阿里云配置信息
    """
    async_session = db_getter()
    session = await async_session.__anext__()
    datas = await SettingsTabDal(session).get_classify_tab_values(["aliyun"], hidden=None)
    assert isinstance(rd, Redis)
    for k, v in datas.items():
        await rd.client().set(k, json.dumps(v))
