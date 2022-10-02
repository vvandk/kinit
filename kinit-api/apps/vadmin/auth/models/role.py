#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : role.py
# @IDE            : PyCharm
# @desc           : 角色模型

from sqlalchemy.orm import relationship
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, Integer
from .m2m import vadmin_user_roles, vadmin_role_menus


class VadminRole(BaseModel):
    __tablename__ = "vadmin_auth_role"
    __table_args__ = ({'comment': '角色表'})

    name = Column(String(50), index=True, nullable=False, comment="名称")
    role_key = Column(String(50), index=True, nullable=False, comment="权限字符")
    disabled = Column(Boolean, default=False, comment="是否禁用")
    order = Column(Integer, comment="排序")
    desc = Column(String(255), comment="描述")
    is_admin = Column(Boolean, comment="是否为超级角色", default=False)

    users = relationship("VadminUser", back_populates='roles', secondary=vadmin_user_roles)
    menus = relationship("VadminMenu", back_populates='roles', secondary=vadmin_role_menus)
