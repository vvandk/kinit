# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from typing import Optional
from fastapi import APIRouter, Depends, Query
from core.dependencies import paging, Params
from utils.response import SuccessResponse
from . import crud
from apps.vadmin.auth.utils.current import login_auth, Auth

app = APIRouter()


###########################################################
#    登录日志管理
###########################################################
@app.get("/login/", summary="获取登录日志列表")
async def get_users(params: Params = Depends(paging), auth: Auth = Depends(login_auth),
                    telephone: Optional[str] = Query(None, title="手机号", description="查询手机号")):
    datas = await crud.LoginRecordDal(auth.db).\
        get_datas(params.page, params.limit, telephone=telephone, order="desc")
    count = await crud.LoginRecordDal(auth.db).get_count(telephone=telephone)
    return SuccessResponse(datas, count=count)


###########################################################
#    短信发送管理
###########################################################
@app.get("/sms/send/list/", summary="获取短信发送列表")
async def get_sms_send_list(params: Params = Depends(paging), auth: Auth = Depends(login_auth),
                            telephone: Optional[str] = Query(None, title="手机号", description="查询手机号")):
    datas = await crud.SMSSendRecordDal(auth.db).get_datas(params.page, params.limit, telephone=telephone, order="desc")
    count = await crud.SMSSendRecordDal(auth.db).get_count(telephone=telephone)
    return SuccessResponse(datas, count=count)
