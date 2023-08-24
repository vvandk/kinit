# -*- coding: utf-8 -*-
# @version        : 1.0
# @Update Time    : 2023/8/18 9:00
# @File           : database.py
# @IDE            : PyCharm
# @desc           : SQLAlchemy 部分

"""
导入 SQLAlchemy 部分
安装： pip install sqlalchemy[asyncio]
官方文档：https://docs.sqlalchemy.org/en/20/intro.html#installation
"""
from typing import AsyncGenerator
from aioredis import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr
from application.settings import SQLALCHEMY_DATABASE_URL, REDIS_DB_ENABLE, MONGO_DB_ENABLE
from fastapi import Request
from core.exception import CustomException
from motor.motor_asyncio import AsyncIOMotorDatabase


def create_async_engine_session(database_url: str) -> async_sessionmaker[AsyncSession]:
    """
    创建数据库会话

    相关配置文档：https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls

    database_url  dialect+driver://username:password@host:port/database
    max_overflow 超过连接池大小外最多创建的连接
    pool_size=5,     # 连接池大小
    pool_timeout=20, # 池中没有连接最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）

    :param database_url: 数据库地址
    :return:
    """
    async_engine = create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=3600,
        future=True,
        max_overflow=5,
        connect_args={}
    )
    return async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        expire_on_commit=True,
        class_=AsyncSession
    )


class Base(AsyncAttrs, DeclarativeBase):
    """
    创建基本映射类
    稍后，我们将继承该类，创建每个 ORM 模型
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        将表名改为小写
        如果有自定义表名就取自定义，没有就取小写类名
        """
        table_name = cls.__tablename__
        if not table_name:
            model_name = cls.__name__
            ls = []
            for index, char in enumerate(model_name):
                if char.isupper() and index != 0:
                    ls.append("_")
                ls.append(char)
            table_name = "".join(ls).lower()
        return table_name


async def db_getter() -> AsyncGenerator[AsyncSession, None]:
    """
    获取主数据库

    数据库依赖项，它将在单个请求中使用，然后在请求完成后将其关闭。

    函数的返回类型被注解为 AsyncGenerator[int, None]，其中 AsyncSession 是生成的值的类型，而 None 表示异步生成器没有终止条件。
    """
    async with create_async_engine_session(SQLALCHEMY_DATABASE_URL)() as session:
        # 创建一个新的事务，半自动 commit
        async with session.begin():
            yield session


def redis_getter(request: Request) -> Redis:
    """
    获取 redis 数据库对象

    全局挂载，使用一个数据库对象
    """
    if not REDIS_DB_ENABLE:
        raise CustomException("请先配置Redis数据库链接并启用！", desc="请启用 application/settings.py: REDIS_DB_ENABLE")
    return request.app.state.redis


def mongo_getter(request: Request) -> AsyncIOMotorDatabase:
    """
    获取 mongo 数据库对象

    全局挂载，使用一个数据库对象
    """
    if not MONGO_DB_ENABLE:
        raise CustomException(msg="请先开启 MongoDB 数据库连接！", desc="请启用 application/settings.py: MONGO_DB_ENABLE")
    return request.app.state.mongo

