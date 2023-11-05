#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : menu.py
# @IDE            : PyCharm
# @desc           : 菜单模型


from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class VadminMenu(BaseModel):
    __tablename__ = "vadmin_auth_menu"
    __table_args__ = ({'comment': '菜单表'})

    title: Mapped[str] = mapped_column(String(50), comment="名称")
    icon: Mapped[str | None] = mapped_column(String(50), comment="菜单图标")
    redirect: Mapped[str | None] = mapped_column(String(100), comment="重定向地址")
    component: Mapped[str | None] = mapped_column(String(255), comment="前端组件地址")
    path: Mapped[str | None] = mapped_column(String(50), comment="前端路由地址")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    hidden: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否隐藏")
    order: Mapped[int] = mapped_column(Integer, comment="排序")
    menu_type: Mapped[str] = mapped_column(String(8), comment="菜单类型")
    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_menu.id", ondelete='CASCADE'),
        comment="父菜单"
    )
    perms: Mapped[str | None] = mapped_column(String(50), comment="权限标识", unique=False, index=True)

    """以下属性主要用于补全前端路由属性，"""
    noCache: Mapped[bool] = mapped_column(
        Boolean,
        comment="如果设置为true，则不会被 <keep-alive> 缓存(默认 false)",
        default=False
    )
    breadcrumb: Mapped[bool] = mapped_column(
        Boolean,
        comment="如果设置为false，则不会在breadcrumb面包屑中显示(默认 true)",
        default=True
    )
    affix: Mapped[bool] = mapped_column(
        Boolean,
        comment="如果设置为true，则会一直固定在tag项中(默认 false)",
        default=False
    )
    noTagsView: Mapped[bool] = mapped_column(
        Boolean,
        comment="如果设置为true，则不会出现在tag中(默认 false)",
        default=False
    )
    canTo: Mapped[bool] = mapped_column(
        Boolean,
        comment="设置为true即使hidden为true，也依然可以进行路由跳转(默认 false)",
        default=False
    )
    alwaysShow: Mapped[bool] = mapped_column(
        Boolean,
        comment="""当你一个路由下面的 children 声明的路由大于1个时，自动会变成嵌套的模式，
    只有一个时，会将那个子路由当做根路由显示在侧边栏，若你想不管路由下面的 children 声明的个数都显示你的根路由，
    你可以设置 alwaysShow: true，这样它就会忽略之前定义的规则，一直显示根路由(默认 true)""",
        default=True
    )
