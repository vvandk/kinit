#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : role.py
# @IDE            : PyCharm
# @desc           : 角色模型

from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer
from .menu import VadminMenu
from .m2m import vadmin_auth_role_menus


class VadminRole(BaseModel):
    __tablename__ = "vadmin_auth_role"
    __table_args__ = ({'comment': '角色表'})

    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="名称")
    role_key: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="权限字符")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    order: Mapped[int | None] = mapped_column(Integer, comment="排序")
    desc: Mapped[str | None] = mapped_column(String(255), comment="描述")
    is_admin: Mapped[bool] = mapped_column(Boolean, comment="是否为超级角色", default=False)

    menus: Mapped[set[VadminMenu]] = relationship(secondary=vadmin_auth_role_menus)
