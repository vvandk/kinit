#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : menu.py
# @IDE            : PyCharm
# @desc           : 菜单模型


from sqlalchemy.orm import relationship
from .m2m import vadmin_role_menus
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey


class VadminMenu(BaseModel):
    __tablename__ = "vadmin_auth_menu"
    __table_args__ = ({'comment': '菜单表'})

    # class MenuTypes(Enum):
    #     dir = "0"
    #     menu = "1"
    #     button = "2"

    title = Column(String(50), index=True, nullable=False, comment="名称")
    icon = Column(String(50), comment="菜单图标")
    redirect = Column(String(100), comment="重定向地址")
    component = Column(String(50), comment="前端组件地址")
    path = Column(String(50), comment="前端路由地址")
    disabled = Column(Boolean, default=False, comment="是否禁用")
    hidden = Column(Boolean, default=False, comment="是否显示")
    order = Column(Integer, comment="排序")
    menu_type = Column(String(8), comment="菜单类型")
    parent_id = Column(ForeignKey("vadmin_auth_menu.id", ondelete='CASCADE'), comment="父菜单")
    perms = Column(String(50), comment="权限标识", unique=False, nullable=True, index=True)
    noCache = Column(Boolean, comment="如果设置为true，则不会被 <keep-alive> 缓存(默认 false)", default=False)
    breadcrumb = Column(Boolean, comment="如果设置为false，则不会在breadcrumb面包屑中显示(默认 true)", default=True)
    affix = Column(Boolean, comment="如果设置为true，则会一直固定在tag项中(默认 false)", default=False)
    noTagsView = Column(Boolean, comment="如果设置为true，则不会出现在tag中(默认 false)", default=False)
    canTo = Column(Boolean, comment="设置为true即使hidden为true，也依然可以进行路由跳转(默认 false)", default=False)

    roles = relationship("VadminRole", back_populates='menus', secondary=vadmin_role_menus)
