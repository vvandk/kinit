# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : auth.py
# @IDE            : PyCharm
# @desc           : 用户凭证验证装饰器

from fastapi import Request, Depends
from jose import jwt, JWTError
from pydantic import BaseModel
from application import settings
from sqlalchemy.ext.asyncio import AsyncSession
from apps.vadmin.auth import models
from core.database import db_getter
from core.exception import CustomException
from utils import status


class Auth(BaseModel):
    user: models.VadminUser = None
    db: AsyncSession

    class Config:
        arbitrary_types_allowed = True


class AuthValidation:

    """
    验证提交 Token 与用户是否有效
    """

    def __init__(self, func):
        self.func = func

    async def __call__(self, request: Request, token: str = Depends(settings.oauth2_scheme),
                       db: AsyncSession = Depends(db_getter)):
        if not settings.OAUTH_ENABLE:
            return Auth(db=db)
        if not token:
            raise CustomException(msg="请先登录！", code=status.HTTP_ERROR)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            telephone: str = payload.get("sub")
            if telephone is None:
                raise CustomException(msg="无效 Token！", code=status.HTTP_403_FORBIDDEN)
        except JWTError:
            raise CustomException(msg="无效 Token！", code=status.HTTP_403_FORBIDDEN)
        user = await self.func(telephone, db)
        if user is None:
            raise CustomException(msg="用户不存在！", code=status.HTTP_404_NOT_FOUND)
        elif not user.is_active:
            raise CustomException(msg="用户已被冻结！", code=status.HTTP_403_FORBIDDEN)
        elif user.is_cancel:
            raise CustomException(msg="用户已被注销！", code=status.HTTP_403_FORBIDDEN)
        request.scope["telephone"] = user.telephone
        try:
            request.scope["body"] = await request.body()
        except RuntimeError:
            request.scope["body"] = "获取失败"
        return Auth(user=user, db=db)
