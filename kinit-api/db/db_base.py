# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : db_base.py
# @IDE            : PyCharm
# @desc           : 数据库公共 ORM 模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from sqlalchemy import DateTime, Integer, func, Boolean


# 使用命令：alembic init alembic 初始化迁移数据库环境
# 这时会生成alembic文件夹 和 alembic.ini文件
class BaseModel(Base):
    """
    公共 ORM 模型，基表
    """
    __abstract__ = True

    id:  Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键ID')
    create_datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment='创建时间')
    update_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间'
    )
    delete_datetime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment='删除时间')
    is_delete: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否软删除")
