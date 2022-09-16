# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19 
# @File           : database.py
# @IDE            : PyCharm
# @desc           : SQLAlchemy 部分

"""
导入 SQLAlchemy 部分
安装： pip install sqlalchemy
中文文档：https://www.osgeo.cn/sqlalchemy/
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import sessionmaker
from application.settings import SQLALCHEMY_DATABASE_URL, DEBUG, SQLALCHEMY_DATABASE_TYPE


def create_async_engine_session(database_url: str, database_type: str = "mysql"):
    """
    创建数据库会话

    相关配置文档：https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls

    database_url  dialect+driver://username:password@host:port/database
    max_overflow 超过连接池大小外最多创建的连接
    pool_size=5,     # 连接池大小
    pool_timeout=20, # 池中没有连接最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）

    :param database_type: 数据库类型
    :param database_url: 数据库地址
    :return:
    """
    engine = create_async_engine(
        database_url
        , echo=False
        , pool_pre_ping=True
        , pool_recycle=3600
        , future=True
        , max_overflow=5
        , connect_args={"check_same_thread": False, "timeout": 30} if database_type == "sqlite3" else {}
    )
    return sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True, class_=AsyncSession)


class Base:
    """将表名改为小写"""

    @declared_attr
    def __tablename__(self):
        # 如果有自定义表名就取自定义，没有就取小写类名
        table_name = self.__tablename__
        if not table_name:
            model_name = self.__name__
            ls = []
            for index, char in enumerate(model_name):
                if char.isupper() and index != 0:
                    ls.append("_")
                ls.append(char)
            table_name = "".join(ls).lower()
        return table_name


"""
创建基本映射类
稍后，我们将继承该类，创建每个 ORM 模型
"""
Model = declarative_base(name='Model', cls=Base)

""" 附上两个SQLAlchemy教程

Python3+SQLAlchemy+Sqlite3实现ORM教程
    https://www.cnblogs.com/jiangxiaobo/p/12350561.html

SQLAlchemy基础知识 Autoflush和Autocommit
    https://www.jianshu.com/p/b219c3dd4d1e
"""


async def db_getter() -> AsyncSession:
    """
    获取主数据库

    数据库依赖项，它将在单个请求中使用，然后在请求完成后将其关闭。
    """
    async with create_async_engine_session(SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_TYPE)() as session:
        async with session.begin():
            yield session
