#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/8/8 14:18 
# @File           : dependencies.py
# @IDE            : PyCharm
# @desc           : 常用依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""

from typing import List
from fastapi import Body
import copy


class Paging:
    """
    列表分页
    """
    def __init__(self, page: int = 1, limit: int = 10):
        self.page = page
        self.limit = limit
        self.order = None

    def dict(self):
        return self.__dict__

    def to_count(self):
        params = copy.deepcopy(self.__dict__)
        del params["page"]
        del params["limit"]
        del params["order"]
        return params


class IdList:
    """
    id 列表
    """
    def __init__(self, ids: List[int] = Body(None, title="ID 列表")):
        self.ids = ids
