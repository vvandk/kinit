# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
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
from redis.asyncio import Redis
from fastapi import APIRouter, Depends, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter, redis_getter
from core.exception import CustomException
from utils import status
from utils.response import SuccessResponse, ErrorResponse
from application import settings
from .login_manage import LoginManage
from .validation import LoginForm, WXLoginForm
from apps.vadmin.record.models import VadminLoginRecord
from apps.vadmin.auth.crud import MenuDal, UserDal
from apps.vadmin.auth.models import VadminUser
from .current import FullAdminAuth
from .validation.auth import Auth
from utils.wx.oauth import WXOAuth
import jwt


app = APIRouter()


@app.post("/api/login", summary="API 手机号密码登录", description="Swagger API 文档登录认证")
async def api_login_for_access_token(
        request: Request,
        data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(db_getter)
):
    user = await UserDal(db).get_data(telephone=data.username, v_return_none=True)
    if not user:
        raise CustomException(status_code=401, code=401, msg="该手机号不存在")
    result = VadminUser.verify_password(data.password, user.password)
    if not result:
        raise CustomException(status_code=401, code=401, msg="手机号或密码错误")
    if not user.is_active:
        raise CustomException(status_code=401, code=401, msg="此手机号已被冻结")
    elif not user.is_staff:
        raise CustomException(status_code=401, code=401, msg="此手机号无权限")
    access_token = LoginManage.create_token({"sub": user.telephone})
    record = LoginForm(platform='2', method='0', telephone=data.username, password=data.password)
    resp = {"access_token": access_token, "token_type": "bearer"}
    await VadminLoginRecord.create_login_record(db, record, True, request, resp)
    return resp


@app.post("/login", summary="手机号密码登录", description="员工登录通道，限制最多输错次数，达到最大值后将is_active=False")
async def login_for_access_token(
        request: Request,
        data: LoginForm,
        manage: LoginManage = Depends(),
        db: AsyncSession = Depends(db_getter)
):
    try:
        if data.method == "0":
            result = await manage.password_login(data, db, request)
        elif data.method == "1":
            result = await manage.sms_login(data, db, request)
        else:
            raise ValueError("无效参数")

        if not result.status:
            raise ValueError(result.msg)

        access_token = LoginManage.create_token({"sub": result.user.telephone, "is_refresh": False})
        expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = LoginManage.create_token({"sub": result.user.telephone, "is_refresh": True}, expires=expires)
        resp = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "is_reset_password": result.user.is_reset_password,
            "is_wx_server_openid": result.user.is_wx_server_openid
        }
        await VadminLoginRecord.create_login_record(db, data, True, request, resp)
        return SuccessResponse(resp)
    except ValueError as e:
        await VadminLoginRecord.create_login_record(db, data, False, request, {"message": str(e)})
        return ErrorResponse(msg=str(e))


@app.post("/wx/login", summary="微信服务端一键登录", description="员工登录通道")
async def wx_login_for_access_token(
        request: Request,
        data: WXLoginForm,
        db: AsyncSession = Depends(db_getter),
        rd: Redis = Depends(redis_getter)
):
    try:
        if data.platform != "1" or data.method != "2":
            raise ValueError("无效参数")
        wx = WXOAuth(rd, 0)
        telephone = await wx.parsing_phone_number(data.code)
        if not telephone:
            raise ValueError("无效Code")
        data.telephone = telephone
        user = await UserDal(db).get_data(telephone=telephone, v_return_none=True)
        if not user:
            raise ValueError("手机号不存在")
        elif not user.is_active:
            raise ValueError("手机号已被冻结")
    except ValueError as e:
        await VadminLoginRecord.create_login_record(db, data, False, request, {"message": str(e)})
        return ErrorResponse(msg=str(e))

    # 更新登录时间
    await UserDal(db).update_login_info(user, request.client.host)

    # 登录成功创建 token
    access_token = LoginManage.create_token({"sub": user.telephone, "is_refresh": False})
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = LoginManage.create_token({"sub": user.telephone, "is_refresh": True}, expires=expires)
    resp = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "is_reset_password": user.is_reset_password,
        "is_wx_server_openid": user.is_wx_server_openid
    }
    await VadminLoginRecord.create_login_record(db, data, True, request, resp)
    return SuccessResponse(resp)


@app.get("/getMenuList", summary="获取当前用户菜单树")
async def get_menu_list(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await MenuDal(auth.db).get_routers(auth.user))


@app.post("/token/refresh", summary="刷新Token")
async def token_refresh(refresh: str = Body(..., title="刷新Token")):
    error_code = status.HTTP_401_UNAUTHORIZED
    try:
        payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        telephone: str = payload.get("sub")
        is_refresh: bool = payload.get("is_refresh")
        if telephone is None or not is_refresh:
            return ErrorResponse("未认证，请您重新登录", code=error_code, status=error_code)
    except jwt.exceptions.InvalidSignatureError:
        return ErrorResponse("无效认证，请您重新登录", code=error_code, status=error_code)
    except jwt.exceptions.ExpiredSignatureError:
        return ErrorResponse("登录已超时，请您重新登录", code=error_code, status=error_code)

    access_token = LoginManage.create_token({"sub": telephone, "is_refresh": False})
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = LoginManage.create_token({"sub": telephone, "is_refresh": True}, expires=expires)
    resp = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    return SuccessResponse(resp)
