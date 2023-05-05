#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : role.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

# pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526


from typing import Optional, List
from pydantic import BaseModel
from core.data_types import DatetimeStr


class Menu(BaseModel):
    title: str
    icon: Optional[str] = None
    component: Optional[str] = None
    redirect: Optional[str] = None
    path: Optional[str] = None
    disabled: bool = False
    hidden: bool = False
    order: Optional[int] = None
    perms: Optional[str] = None
    parent_id: Optional[int] = None
    menu_type: str
    alwaysShow: Optional[bool] = True


class MenuSimpleOut(Menu):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    class Config:
        orm_mode = True


class Meta(BaseModel):
    title: str
    icon: Optional[str] = None
    hidden: bool = False
    noCache: Optional[bool] = False
    breadcrumb: Optional[bool] = True
    affix: Optional[bool] = False
    noTagsView: Optional[bool] = False
    canTo: Optional[bool] = False
    alwaysShow: Optional[bool] = True


# 路由展示
class RouterOut(BaseModel):
    name: Optional[str] = None
    component: Optional[str] = None
    path: str
    redirect: Optional[str] = None
    meta: Optional[Meta] = None
    order: Optional[int] = None
    children: List['RouterOut'] = []

    class Config:
        orm_mode = True


RouterOut.update_forward_refs()


class TreeListOut(MenuSimpleOut):
    children: List['TreeListOut'] = []

    class Config:
        orm_mode = True


RouterOut.update_forward_refs()
