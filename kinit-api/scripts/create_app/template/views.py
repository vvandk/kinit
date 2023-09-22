#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : {create_datetime}
# @File           : views.py
# @IDE            : PyCharm
# @desc           :


from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import schemas, crud, models

app = APIRouter()


