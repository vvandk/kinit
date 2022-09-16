#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/8/8 14:18 
# @File           : dependencies.py
# @IDE            : PyCharm
# @desc           : 常用依赖项

from typing import List
from fastapi import Body
from pydantic import BaseModel


class Params(BaseModel):
    page: int
    limit: int


async def paging(page: int = 1, limit: int = 10) -> Params:
    """
    分页依赖项
    """
    return Params(page=page, limit=limit)


async def id_list(ids: List[int] = Body(None, title="ID 列表")) -> list:
    """
    id 列表
    """
    return ids
