#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : user.py
# @IDE            : PyCharm
# @desc           : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class UserParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str | None = Query(None, title="用户名称"),
            telephone: str | None = Query(None, title="手机号"),
            email: str | None = Query(None, title="邮箱"),
            is_active: bool | None = Query(None, title="是否可用"),
            is_staff: bool | None = Query(None, title="是否为工作人员"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.telephone = ("like", telephone)
        self.email = ("like", email)
        self.is_active = is_active
        self.is_staff = is_staff


