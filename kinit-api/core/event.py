#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/3/21 11:03 
# @File           : event.py
# @IDE            : PyCharm
# @desc           : 全局事件


from fastapi import FastAPI
from aioredis import from_url
from application.settings import REDIS_DB_URL, MONGO_DB_URL, MONGO_DB_NAME
from core.mongo import db
from utils.cache import Cache


def register_redis(app: FastAPI) -> None:
    """
    把 redis 挂载到 app 对象上面

    博客：https://blog.csdn.net/wgPython/article/details/107668521
    博客：https://www.cnblogs.com/emunshe/p/15761597.html
    官网：https://aioredis.readthedocs.io/en/latest/getting-started/
    :param app:
    :return:
    """

    @app.on_event('startup')
    async def startup_event():
        """
        获取链接
        :return:
        """
        print("Connecting to Redis")
        app.state.redis = from_url(REDIS_DB_URL, decode_responses=True, health_check_interval=1)
        await Cache(app.state.redis).cache_tab_names()

    @app.on_event('shutdown')
    async def shutdown_event():
        """
        关闭
        :return:
        """
        print("Redis connection closed")
        await app.state.redis.close()


def register_mongo(app: FastAPI) -> None:
    """
    把 mongo 挂载到 app 对象上面

    博客：https://www.cnblogs.com/aduner/p/13532504.html
    mongodb 官网：https://www.mongodb.com/docs/drivers/motor/
    motor 文档：https://motor.readthedocs.io/en/stable/
    :param app:
    :return:
    """

    @app.on_event('startup')
    async def startup_event():
        """
        获取 mongodb 连接
        :return:
        """
        await db.connect_to_database(path=MONGO_DB_URL, db_name=MONGO_DB_NAME)

    @app.on_event('shutdown')
    async def shutdown_event():
        """
        关闭
        :return:
        """
        await db.close_database_connection()
