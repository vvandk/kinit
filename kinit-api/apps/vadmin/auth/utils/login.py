# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 安全认证视图

"""
JWT 表示 「JSON Web Tokens」。https://jwt.io/

它是一个将 JSON 对象编码为密集且没有空格的长字符串的标准。

通过这种方式，你可以创建一个有效期为 1 周的令牌。然后当用户第二天使用令牌重新访问时，你知道该用户仍然处于登入状态。
一周后令牌将会过期，用户将不会通过认证，必须再次登录才能获得一个新令牌。

我们需要安装 python-jose 以在 Python 中生成和校验 JWT 令牌：pip install python-jose[cryptography]

PassLib 是一个用于处理哈希密码的很棒的 Python 包。它支持许多安全哈希算法以及配合算法使用的实用程序。
推荐的算法是 「Bcrypt」：pip install passlib[bcrypt]
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter
from utils.response import SuccessResponse, ErrorResponse
from application import settings
from utils.tools import generate_string
from .login_manage import LoginManage
from .validation import LoginForm, WXLoginForm
from apps.vadmin.record.models import VadminLoginRecord
from apps.vadmin.auth.crud import MenuDal, UserDal
from apps.vadmin.auth.schemas import UserIn
from .current import FullAdminAuth
from .validation.auth import Auth
from utils.wx.oauth import WXOAuth
from core.data_types import Telephone

app = APIRouter()


@app.post("/login/", summary="手机号密码登录")
async def login_for_access_token(
        request: Request,
        data: LoginForm,
        manage: LoginManage = Depends(),
        db: AsyncSession = Depends(db_getter)
):
    if data.method == "0":
        result = await manage.password_login(data, db, request)
    elif data.method == "1":
        result = await manage.sms_login(data, db, request)
    else:
        return ErrorResponse(msg="请使用正确的登录方式")
    if not result.status:
        resp = {"message": result.msg}
        await VadminLoginRecord.create_login_record(db, data, result.status, request, resp)
        return ErrorResponse(msg=result.msg)
    user = result.user

    if data.platform in ["0", "1"] and not user.is_staff:
        msg = "此手机号无登录权限"
        await VadminLoginRecord.create_login_record(db, data, result.status, request, {"message": msg})
        return ErrorResponse(msg=msg)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = LoginManage.create_access_token(data={"sub": user.telephone}, expires_delta=access_token_expires)
    resp = {
        "access_token": access_token,
        "token_type": "bearer",
        "is_reset_password": user.is_reset_password,
        "is_wx_server_openid": user.is_wx_server_openid
    }
    await VadminLoginRecord.create_login_record(db, data, result.status, request, resp)
    return SuccessResponse(resp)


@app.post("/wx/login/", summary="微信服务端一键登录")
async def wx_login_for_access_token(request: Request, data: WXLoginForm, db: AsyncSession = Depends(db_getter)):
    if data.platform not in ["0", "1"]:
        msg = "错误平台"
        await VadminLoginRecord.create_login_record(db, data, False, request, {"message": msg})
        return ErrorResponse(msg=msg)
    wx = WXOAuth(request.app.state.redis, 0)
    telephone = await wx.parsing_phone_number(data.code)
    if not telephone:
        msg = "无效Code"
        await VadminLoginRecord.create_login_record(db, data, False, request, {"message": msg})
        return ErrorResponse(msg=msg)
    data.telephone = telephone
    user = await UserDal(db).get_data(telephone=telephone, v_return_none=True)
    msg = None
    if not user:
        # 手机号不存在，创建新用户
        # model = UserIn(name=generate_string(), telephone=Telephone(telephone))
        # user = await UserDal(db).create_data(model, v_return_obj=True)
        msg = "手机号不存在！"
    elif not user.is_active:
        msg = "此手机号已被冻结！"
    elif data.platform in ["0", "1"] and not user.is_staff:
        msg = "此手机号无登录权限"
    if msg:
        await VadminLoginRecord.create_login_record(db, data, False, request, {"message": msg})
        return ErrorResponse(msg=msg)
    # 更新登录时间
    await user.update_login_info(db, request.client.host)

    # 登录成功创建 token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = LoginManage.create_access_token(data={"sub": user.telephone}, expires_delta=access_token_expires)
    resp = {
        "access_token": access_token,
        "token_type": "bearer",
        "is_reset_password": user.is_reset_password,
        "is_wx_server_openid": user.is_wx_server_openid
    }
    await VadminLoginRecord.create_login_record(db, data, True, request, resp)
    return SuccessResponse(resp)


@app.get("/getMenuList/", summary="获取当前用户菜单树")
async def get_menu_list(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await MenuDal(auth.db).get_routers(auth.user))
