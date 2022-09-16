#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : m2m.py
# @IDE            : PyCharm
# @desc           : 关联中间表

from db.db_base import Model
from sqlalchemy import Column, Table, Integer, ForeignKey, INT


vadmin_user_roles = Table(
    'vadmin_auth_user_roles',
    Model.metadata,
    Column("id", INT, primary_key=True, unique=True, comment='主键ID', index=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('vadmin_auth_user.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey('vadmin_auth_role.id', ondelete='CASCADE'), primary_key=True),
)


vadmin_role_menus = Table(
    'vadmin_auth_role_menus',
    Model.metadata,
    Column("id", INT, primary_key=True, unique=True, comment='主键ID', index=True, autoincrement=True),
    Column('role_id', Integer, ForeignKey('vadmin_auth_role.id', ondelete='CASCADE'), primary_key=True),
    Column('menu_id', Integer, ForeignKey('vadmin_auth_menu.id', ondelete='CASCADE'), primary_key=True),
)
