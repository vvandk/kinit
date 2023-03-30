#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/3/21 11:03
# @File           : cache.py
# @IDE            : PyCharm
# @desc           : 缓存

from typing import List
from core import logger
from core.database import db_getter
from apps.vadmin.system.crud import SettingsTabDal
import json
from aioredis.client import Redis
from core.exception import CustomException
from utils import status


class Cache:

    DEFAULT_TAB_NAMES = ["wx_server", "aliyun_sms", "aliyun_oss"]

    def __init__(self, rd: Redis):
        self.rd = rd

    async def cache_tab_names(self, tab_names: List[str] = None):
        """
        缓存系统配置
        如果手动修改了mysql数据库中的配置
        那么需要在redis中将对应的tab_name删除
        """
        async_session = db_getter()
        session = await async_session.__anext__()
        if tab_names:
            datas = await SettingsTabDal(session).get_tab_name_values(tab_names, hidden=None)
        else:
            datas = await SettingsTabDal(session).get_tab_name_values(self.DEFAULT_TAB_NAMES, hidden=None)
        for k, v in datas.items():
            await self.rd.client().set(k, json.dumps(v))

    async def get_tab_name(self, tab_name: str, retry: int = 3):
        """
        获取系统配置
        :params tab_name: 配置表标签名称
        :params retry_num: 重试次数
        """
        result = await self.rd.get(tab_name)
        if not result and retry > 0:
            logger.error(f"未从Redis中获取到{tab_name}配置信息，正在重新更新配置信息，重试次数：{retry}。")
            await self.cache_tab_names([tab_name])
            return await self.get_tab_name(tab_name, retry - 1)
        elif not result and retry == 0:
            raise CustomException(f"获取{tab_name}配置信息失败，请联系管理员！", code=status.HTTP_ERROR)
        else:
            return json.loads(result)
