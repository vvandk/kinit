#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : m2m.py
# @IDE            : PyCharm
# @desc           : 关联中间表

from db.db_base import Base
from sqlalchemy import ForeignKey, Column, Table, Integer


vadmin_auth_user_roles = Table(
    "vadmin_auth_user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("vadmin_auth_user.id", ondelete="CASCADE")),
    Column("role_id", Integer, ForeignKey("vadmin_auth_role.id", ondelete="CASCADE")),
)


vadmin_auth_role_menus = Table(
    "vadmin_auth_role_menus",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("vadmin_auth_role.id", ondelete="CASCADE")),
    Column("menu_id", Integer, ForeignKey("vadmin_auth_menu.id", ondelete="CASCADE")),
)

