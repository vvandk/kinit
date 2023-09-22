#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : role.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr


class Menu(BaseModel):
    title: str
    icon: str | None = None
    component: str | None = None
    redirect: str | None = None
    path: str | None = None
    disabled: bool = False
    hidden: bool = False
    order: int | None = None
    perms: str | None = None
    parent_id: int | None = None
    menu_type: str
    alwaysShow: bool | None = True
    noCache: bool | None = False


class MenuSimpleOut(Menu):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class Meta(BaseModel):
    title: str
    icon: str | None = None
    hidden: bool = False
    noCache: bool | None = False
    breadcrumb: bool | None = True
    affix: bool | None = False
    noTagsView: bool | None = False
    canTo: bool | None = False
    alwaysShow: bool | None = True


# 路由展示
class RouterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    component: str | None = None
    path: str
    redirect: str | None = None
    meta: Meta | None = None
    order: int | None = None
    children: list[dict] = []


class TreeListOut(MenuSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    children: list[dict] = []
