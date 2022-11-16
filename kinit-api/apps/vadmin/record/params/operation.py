#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : operation.py
# @IDE            : PyCharm
# @desc           : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""

from core.dependencies import Paging


class OperationParams(Paging):
    """
    列表分页
    """
    def __init__(self, summary: str = None, telephone: str = None, request_method: str = None, page: int = 1,
                 limit: int = 10):
        super(OperationParams, self).__init__(page, limit)
        self.summary = ("like", summary)
        self.telephone = ("like", telephone)
        self.request_method = request_method
