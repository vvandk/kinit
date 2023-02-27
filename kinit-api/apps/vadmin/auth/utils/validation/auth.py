# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : auth.py
# @IDE            : PyCharm
# @desc           : 用户凭证验证装饰器

from fastapi import Request
from jose import jwt, JWTError
from pydantic import BaseModel
from application import settings
from sqlalchemy.ext.asyncio import AsyncSession
from apps.vadmin.auth import models
from core.exception import CustomException
from utils import status


class Auth(BaseModel):
    user: models.VadminUser = None
    db: AsyncSession

    class Config:
        arbitrary_types_allowed = True


class AuthValidation:

    """
    用于用户每次调用接口时，验证用户提交的token是否正确，并从token中获取用户信息
    """

    @classmethod
    def validate_token(cls, token: str, db: AsyncSession) -> str | Auth:
        """
        验证用户 token
        """
        if not settings.OAUTH_ENABLE:
            return Auth(db=db)
        if not token:
            raise CustomException(msg="请您先登录！", code=status.HTTP_ERROR)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            telephone: str = payload.get("sub")
            if telephone is None:
                raise CustomException(msg="认证已过期，请您重新登陆", code=status.HTTP_401_UNAUTHORIZED)
        except JWTError:
            raise CustomException(msg="认证已过期，请您重新登陆", code=status.HTTP_401_UNAUTHORIZED)
        return telephone

    @classmethod
    async def validate_user(cls, request: Request, user: models.VadminUser, db: AsyncSession) -> Auth:
        """
        验证用户信息
        """
        if user is None:
            raise CustomException(msg="认证已过期，请您重新登陆", code=status.HTTP_401_UNAUTHORIZED)
        elif not user.is_active:
            raise CustomException(msg="用户已被冻结！", code=status.HTTP_403_FORBIDDEN)
        request.scope["telephone"] = user.telephone
        try:
            request.scope["body"] = await request.body()
        except RuntimeError:
            request.scope["body"] = "获取失败"
        return Auth(user=user, db=db)
