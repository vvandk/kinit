#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:19
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""

from core.dependencies import Paging


class SMSParams(Paging):
    """
    列表分页
    """
    def __init__(self, telephone: str = None, page: int = 1, limit: int = 10):
        super(SMSParams, self).__init__(page, limit)
        self.telephone = ("like", telephone)
        self.order = "desc"
