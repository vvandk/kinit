#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/25 14:50 
# @File           : task.py
# @IDE            : PyCharm
# @desc           : 简要说明
from fastapi import Depends
from core.dependencies import Paging, QueryParams


class TaskParams(QueryParams):
    """
    列表分页
    """
    def __init__(self, name: str = None, _id: str = None, group: str = None, params: Paging = Depends()):
        super().__init__(params)
        self.name = ("like", name)
        self.group = group
        self._id = ("ObjectId", _id)
        self.v_order = "desc"


class TaskRecordParams(QueryParams):
    """
    列表分页
    """
    def __init__(self, job_id: str = None, name: str = None, params: Paging = Depends()):
        super().__init__(params)
        self.job_id = ("like", job_id)
        self.name = ("like", name)
        self.v_order = "desc"
