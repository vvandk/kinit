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


class QueryParams:

    def __init__(self, params=None):
        if params:
            self.page = params.page
            self.limit = params.limit
            self.v_order = params.v_order
            self.v_order_field = params.v_order_field

    def dict(self) -> dict:
        return self.__dict__

    def to_count(self) -> dict:
        params = copy.deepcopy(self.__dict__)
        del params["page"]
        del params["limit"]
        del params["v_order"]
        del params["v_order_field"]
        return params


class Paging(QueryParams):
    """
    列表分页
    """
    def __init__(self, page: int = 1, limit: int = 10, v_order_field: str = "id", v_order: str = None):
        super().__init__()
        self.page = page
        self.limit = limit
        self.v_order = v_order
        self.v_order_field = v_order_field


class IdList:
    """
    id 列表
    """
    def __init__(self, ids: List[int] = Body(None, title="ID 列表")):
        self.ids = ids
