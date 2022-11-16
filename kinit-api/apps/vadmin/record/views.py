# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from typing import Optional
from fastapi import APIRouter, Depends, Query
from core.dependencies import Paging, IdList
from utils.response import SuccessResponse
from . import crud, schemas
from apps.vadmin.auth.utils.current import login_auth, Auth
from core.mongo import get_database, DatabaseManage
from .params import LoginParams, OperationParams, SMSParams

app = APIRouter()


###########################################################
#    日志管理
###########################################################
@app.get("/logins/", summary="获取登录日志列表")
async def get_record_login(params: LoginParams = Depends(), auth: Auth = Depends(login_auth)):
    datas = await crud.LoginRecordDal(auth.db).get_datas(**params.dict())
    count = await crud.LoginRecordDal(auth.db).get_count(**params.to_count())
    return SuccessResponse(datas, count=count)


@app.get("/operations/", summary="获取操作日志列表")
async def get_record_operation(params: OperationParams = Depends(), db: DatabaseManage = Depends(get_database),
                               auth: Auth = Depends(login_auth)):
    count = await db.get_count("operation_record", **params.to_count())
    datas = await db.get_datas("operation_record", schema=schemas.OpertionRecordSimpleOut, **params.dict())
    return SuccessResponse(datas, count=count)


@app.get("/sms/send/list/", summary="获取短信发送列表")
async def get_sms_send_list(params: SMSParams = Depends(), auth: Auth = Depends(login_auth)):
    datas = await crud.SMSSendRecordDal(auth.db).get_datas(**params.dict())
    count = await crud.SMSSendRecordDal(auth.db).get_count(**params.to_count())
    return SuccessResponse(datas, count=count)
