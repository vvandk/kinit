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

PassLib 是一个用于处理哈希密码的很棒的 Python 包。它支持许多安全哈希算法以及配合算法使用的实用程序。推荐的算法是 「Bcrypt」：pip install passlib[bcrypt]
"""
import json
from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from utils.response import SuccessResponse, ErrorResponse
from application import settings
from .auth_util import authenticate_user, create_access_token
from apps.vadmin.record.models import VadminLoginRecord
from apps.vadmin.auth.crud import MenuDal
from .current import AdminAuth, full_admin

app = APIRouter()


@app.post("/login/", summary="登录")
async def login_for_access_token(request: Request, data: dict = Depends(authenticate_user)):
    if not data.get("status", False):
        await VadminLoginRecord.create_login_record(telephone=data["data"].telephone, status=data.get("status"),
                                                    request=request, response=data.get("msg"), db=data.get("db"))
        return ErrorResponse(msg=data.get("msg"))
    user = data.get("user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.telephone}, expires_delta=access_token_expires
    )
    result = {
        "access_token": access_token,
        "token_type": "bearer",
        "is_reset_password": user.is_reset_password,
        "user": {
            "id": user.id,
            "telephone": user.telephone,
            "name": user.name,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "gender": user.gender,
            "create_datetime": user.create_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "roles": [{"name": i.name, "value": i.role_key} for i in user.roles]
        }
    }
    await VadminLoginRecord.create_login_record(telephone=user.telephone, status=data.get("status"), request=request,
                                                response=json.dumps(result), db=data.get("db"))
    return SuccessResponse(result)


@app.get("/getMenuList/", summary="获取当前用户菜单树")
async def get_menu_list(auth: AdminAuth = Depends(full_admin)):
    datas = await MenuDal(auth.db).get_routers(auth.admin)
    return SuccessResponse(datas)
