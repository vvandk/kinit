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
from fastapi import Depends
from core.dependencies import Paging, QueryParams


class UserParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str | None = None,
            telephone: str | None = None,
            email: str | None = None,
            is_active: bool | None = None,
            is_staff: bool | None = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.telephone = ("like", telephone)
        self.email = ("like", email)
        self.is_active = is_active
        self.is_staff = is_staff


