#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/8/25 14:59
# @File           : images.py
# @IDE            : PyCharm
# @desc           : 简要说明


from fastapi import Depends
from core.dependencies import Paging, QueryParams


class ImagesParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            filename: str = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.filename = ('like', filename)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
