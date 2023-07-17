# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : auth.py
# @IDE            : PyCharm
# @desc           : 用户凭证验证装饰器

from fastapi import Request
import jwt
from pydantic import BaseModel
from application import settings
from sqlalchemy.ext.asyncio import AsyncSession
from apps.vadmin.auth.models import VadminUser
from core.exception import CustomException
from utils import status
from datetime import timedelta, datetime


class Auth(BaseModel):
    user: VadminUser = None
    db: AsyncSession

    class Config:
        # 接收任意类型
        arbitrary_types_allowed = True


class AuthValidation:
    """
    用于用户每次调用接口时，验证用户提交的token是否正确，并从token中获取用户信息
    """

    # status_code = 401 时，表示强制要求重新登录，因账号已冻结，账号已过期，手机号码错误，刷新token无效等问题导致
    # 只有 code = 401 时，表示 token 过期，要求刷新 token
    # 只有 code = 错误值时，只是报错，不重新登陆
    error_code = status.HTTP_401_UNAUTHORIZED
    warning_code = status.HTTP_ERROR

    # status_code = 403 时，表示强制要求重新登录，因无系统权限，而进入到系统访问等问题导致

    @classmethod
    def validate_token(cls, request: Request, token: str | None) -> str:
        """
        验证用户 token
        """
        if not token:
            raise CustomException(
                msg="请您先登录！",
                code=status.HTTP_403_FORBIDDEN,
                status_code=status.HTTP_403_FORBIDDEN
            )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            telephone: str = payload.get("sub")
            exp: int = payload.get("exp")
            is_refresh: bool = payload.get("is_refresh")
            if telephone is None or is_refresh:
                raise CustomException(
                    msg="未认证，请您重新登录",
                    code=status.HTTP_403_FORBIDDEN,
                    status_code=status.HTTP_403_FORBIDDEN
                )
            # 计算当前时间 + 缓冲时间是否大于等于 JWT 过期时间
            buffer_time = (datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_CACHE_MINUTES)).timestamp()
            # print("过期时间", exp, datetime.fromtimestamp(exp))
            # print("当前时间", buffer_time, datetime.fromtimestamp(buffer_time))
            # print("剩余时间", exp - buffer_time)
            if buffer_time >= exp:
                request.scope["if-refresh"] = 1
            else:
                request.scope["if-refresh"] = 0
        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
            raise CustomException(
                msg="无效认证，请您重新登录",
                code=status.HTTP_403_FORBIDDEN,
                status_code=status.HTTP_403_FORBIDDEN
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise CustomException(msg="认证已过期，请您重新登录", code=cls.error_code, status_code=cls.error_code)
        return telephone

    @classmethod
    async def validate_user(cls, request: Request, user: VadminUser, db: AsyncSession) -> Auth:
        """
        验证用户信息
        """
        if user is None:
            raise CustomException(msg="未认证，请您重新登陆", code=cls.error_code, status_code=cls.error_code)
        elif not user.is_active:
            raise CustomException(msg="用户已被冻结！", code=cls.error_code, status_code=cls.error_code)
        request.scope["telephone"] = user.telephone
        request.scope["user_id"] = user.id
        request.scope["user_name"] = user.name
        try:
            request.scope["body"] = await request.body()
        except RuntimeError:
            request.scope["body"] = "获取失败"
        return Auth(user=user, db=db)

    @classmethod
    def get_user_permissions(cls, user: VadminUser) -> set:
        """
        获取员工用户所有权限列表
        """
        if user.is_admin():
            return {'*.*.*'}
        permissions = set()
        for role_obj in user.roles:
            for menu in role_obj.menus:
                if menu.perms and not menu.disabled:
                    permissions.add(menu.perms)
        return permissions
