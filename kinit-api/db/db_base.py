# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : db_base.py
# @IDE            : PyCharm
# @desc           : 数据库公共 ORM 模型


from core.database import Model
from sqlalchemy import Column, DateTime, Integer, func


# 使用命令：alembic init alembic 初始化迁移数据库环境
# 这时会生成alembic文件夹 和 alembic.ini文件
class BaseModel(Model):
    """
    公共 ORM 模型，基表
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, unique=True, comment='主键ID', index=True)
    create_datetime = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_datetime = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')