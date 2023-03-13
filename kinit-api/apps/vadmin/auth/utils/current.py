# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : current.py
# @IDE            : PyCharm
# @desc           : 获取认证后的信息工具
from datetime import datetime, timedelta
from typing import List, Optional
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from apps.vadmin.auth.crud import UserDal
from apps.vadmin.auth.models import VadminUser
from core.exception import CustomException
from utils import status
from .validation import AuthValidation
from fastapi import Request, Depends
from application import settings
from core.database import db_getter
from .validation.auth import Auth


def get_user_permissions(user: VadminUser) -> set:
    """
    获取员工用户所有权限列表
    """
    if any([role.is_admin for role in user.roles]):
        return {'*.*.*'}
    permissions = set()
    for role_obj in user.roles:
        for menu in role_obj.menus:
            if menu.perms and not menu.disabled:
                permissions.add(menu.perms)
    return permissions


class OpenAuth(AuthValidation):

    """
    开放认证，无认证也可以访问
    认证了以后可以获取到用户信息，无认证则获取不到
    """

    @classmethod
    def validate_token(cls, request: Request, token: str | None) -> str | None:
        """
        验证用户 token，没有则返回 None
        """
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            telephone: str = payload.get("sub")
            exp: int = payload.get("exp")
            is_refresh: bool = payload.get("is_refresh")
            if telephone is None or is_refresh:
                return None
            # 计算当前时间 + 缓冲时间是否大于等于 JWT 过期时间
            buffer_time = (datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_CACHE_MINUTES)).timestamp()
            if buffer_time >= exp:
                request.scope["refresh"] = True
            else:
                request.scope["refresh"] = False
        except jwt.exceptions.InvalidSignatureError:
            return None
        except jwt.exceptions.ExpiredSignatureError:
            return None
        return telephone

    @classmethod
    async def validate_user(cls, request: Request, user: VadminUser, db: AsyncSession) -> Auth:
        """
        验证用户信息
        """
        if user is None:
            return Auth(db=db)
        elif not user.is_active:
            return Auth(db=db)
        request.scope["telephone"] = user.telephone
        try:
            request.scope["body"] = await request.body()
        except RuntimeError:
            request.scope["body"] = "获取失败"
        return Auth(user=user, db=db)

    async def __call__(
            self,
            request: Request,
            token: str = Depends(settings.oauth2_scheme),
            db: AsyncSession = Depends(db_getter)
    ):
        """
        每次调用依赖此类的接口会执行该方法
        """
        telephone = self.validate_token(request, token)
        if telephone:
            user = await UserDal(db).get_data(telephone=telephone, v_return_none=True)
            return await self.validate_user(request, user, db)
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
        if isinstance(telephone, Auth):
            return telephone
        user = await UserDal(db).get_data(telephone=telephone, v_return_none=True)
        return await self.validate_user(request, user, db)


class FullAdminAuth(AuthValidation):

    """
    只支持员工用户认证
    获取员工用户完整信息
    如果有权限，那么会验证该用户是否包括权限列表中的其中一个权限
    """

    def __init__(self, permissions: Optional[List[str]] = None):
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
        if isinstance(telephone, Auth):
            return telephone
        options = [joinedload(VadminUser.roles), joinedload("roles.menus")]
        user = await UserDal(db).get_data(telephone=telephone, v_return_none=True, v_options=options, is_staff=True)
        result = await self.validate_user(request, user, db)
        permissions = get_user_permissions(user)
        if permissions != {'*.*.*'} and self.permissions:
            if not (self.permissions & permissions):
                raise CustomException(msg="无权限操作", code=status.HTTP_403_FORBIDDEN)
        return result

