#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : {create_datetime}
# @File           : views.py
# @IDE            : PyCharm
# @desc           :


from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import schemas, crud, models
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import login_auth, Auth

app = APIRouter()


