# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import crud, schemas
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.mongo import get_database, DatabaseManage
from .params import LoginParams, OperationParams, SMSParams

app = APIRouter()


###########################################################
#    日志管理
###########################################################
@app.get("/logins/", summary="获取登录日志列表")
async def get_record_login(p: LoginParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas = await crud.LoginRecordDal(auth.db).get_datas(**p.dict())
    count = await crud.LoginRecordDal(auth.db).get_count(**p.to_count())
    return SuccessResponse(datas, count=count, refresh=auth.refresh)


@app.get("/operations/", summary="获取操作日志列表")
async def get_record_operation(p: OperationParams = Depends(), db: DatabaseManage = Depends(get_database),
                               auth: Auth = Depends(AllUserAuth())):
    count = await db.get_count("operation_record", **p.to_count())
    datas = await db.get_datas("operation_record", v_schema=schemas.OpertionRecordSimpleOut, **p.dict())
    return SuccessResponse(datas, count=count, refresh=auth.refresh)


@app.get("/sms/send/list/", summary="获取短信发送列表")
async def get_sms_send_list(p: SMSParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas = await crud.SMSSendRecordDal(auth.db).get_datas(**p.dict())
    count = await crud.SMSSendRecordDal(auth.db).get_count(**p.to_count())
    return SuccessResponse(datas, count=count, refresh=auth.refresh)


###########################################################
#    日志分析
###########################################################
@app.get("/analysis/user/login/distribute/", summary="获取用户登录分布情况列表")
async def get_user_login_distribute(auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.LoginRecordDal(auth.db).get_user_distribute(), refresh=auth.refresh)
