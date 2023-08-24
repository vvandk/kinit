# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : current.py
# @IDE            : PyCharm
# @desc           : 获取认证后的信息工具

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from apps.vadmin.auth.crud import UserDal
from apps.vadmin.auth.models import VadminUser, VadminRole
from core.exception import CustomException
from utils import status
from .validation import AuthValidation
from fastapi import Request, Depends
from application import settings
from core.database import db_getter
from .validation.auth import Auth


class OpenAuth(AuthValidation):

    """
    开放认证，无认证也可以访问
    认证了以后可以获取到用户信息，无认证则获取不到
    """

    async def __call__(
            self,
            request: Request,
            token: Annotated[str, Depends(settings.oauth2_scheme)],
            db: AsyncSession = Depends(db_getter)
    ):
        """
        每次调用依赖此类的接口会执行该方法
        """
        if not settings.OAUTH_ENABLE:
            return Auth(db=db)
        try:
            telephone = self.validate_token(request, token)
            user = await UserDal(db).get_data(telephone=telephone, v_return_none=True)
            return await self.validate_user(request, user, db)
        except CustomException:
            return Auth(db=db)


class AllUserAuth(AuthValidation):

    """
    支持所有用户认证
    获取用户基本信息
    """

    async def __call__(
            self,
            request: Request,
            token: str = Depends(settings.oauth2_scheme),
            db: AsyncSession = Depends(db_getter)
    ):
        """
        每次调用依赖此类的接口会执行该方法
        """
        if not settings.OAUTH_ENABLE:
            return Auth(db=db)
        telephone = self.validate_token(request, token)
        user = await UserDal(db).get_data(telephone=telephone, v_return_none=True)
        return await self.validate_user(request, user, db)


class FullAdminAuth(AuthValidation):

    """
    只支持员工用户认证
    获取员工用户完整信息
    如果有权限，那么会验证该用户是否包括权限列表中的其中一个权限
    """

    def __init__(self, permissions: list[str] | None = None):
        if permissions:
            self.permissions = set(permissions)
        else:
            self.permissions = None

    async def __call__(
            self,
            request: Request,
            token: str = Depends(settings.oauth2_scheme),
            db: AsyncSession = Depends(db_getter)
    ) -> Auth:
        """
        每次调用依赖此类的接口会执行该方法
        """
        if not settings.OAUTH_ENABLE:
            return Auth(db=db)
        telephone = self.validate_token(request, token)
        options = [joinedload(VadminUser.roles).subqueryload(VadminRole.menus)]
        user = await UserDal(db).get_data(telephone=telephone, v_return_none=True, v_options=options, is_staff=True)
        result = await self.validate_user(request, user, db)
        permissions = self.get_user_permissions(user)
        if permissions != {'*.*.*'} and self.permissions:
            if not (self.permissions & permissions):
                raise CustomException(msg="无权限操作", code=status.HTTP_403_FORBIDDEN)
        return result

