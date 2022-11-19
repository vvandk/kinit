#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : login.py
# @IDE            : PyCharm
# @desc           : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""

from core.dependencies import Paging


class LoginParams(Paging):
    """
    列表分页
    """
    def __init__(self, ip: str = None, address: str = None, telephone: str = None, status: bool = None, page: int = 1,
                 limit: int = 10):
        super(LoginParams, self).__init__(page, limit)
        self.ip = ("like", ip)
        self.telephone = ("like", telephone)
        self.address = ("like", address)
        self.status = status
        self.order = "desc"
