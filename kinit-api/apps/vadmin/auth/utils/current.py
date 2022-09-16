# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : current.py
# @IDE            : PyCharm
# @desc           : 获取认证后的信息工具


from fastapi import Depends
from pydantic import BaseModel
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter
from application import settings
from jose import JWTError, jwt
from apps.vadmin.auth import crud, models
from core.exception import CustomException


async def get_user_permissions(user: models.VadminUser, db: AsyncSession):
    """
    获取跟进系统用户所有权限列表
    """
    roles = []
    for i in user.roles:
        if i.is_admin:
            return ["*:*:*"]
        roles.append(i.id)
    permissions = set()
    for data_id in roles:
        role_obj = await crud.RoleDal(db).get_data(data_id, options=[models.VadminUser])
        for menu in role_obj.menus:
            if menu.perms and menu.status:
                permissions.add(menu.perms)
    return list(permissions)


class Auth(BaseModel):
    user: models.VadminUser = None
    db: AsyncSession

    class Config:
        arbitrary_types_allowed = True


async def login_auth(token: str = Depends(settings.oauth2_scheme), db: AsyncSession = Depends(db_getter)):
    """
    更新 login_auth 以接收 JWT 令牌。

    解码接收到的令牌，对其进行校验，然后返回当前用户。

    如果令牌无效，立即返回一个 HTTP 错误。
    """
    if not settings.OAUTH_ENABLE:
        return Auth(db=db)
    if not token:
        raise CustomException(msg="请先登录！", code=status.HTTP_403_FORBIDDEN)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        telephone: str = payload.get("sub")
        if telephone is None:
            raise CustomException(msg="无效 Token！", code=status.HTTP_403_FORBIDDEN)
    except JWTError:
        raise CustomException(msg="无效 Token！", code=status.HTTP_403_FORBIDDEN)
    user = await crud.UserDal(db).get_data(telephone=telephone, return_none=True)
    if user is None:
        raise CustomException(msg="用户不存在！", code=status.HTTP_404_NOT_FOUND)
    elif not user.is_active:
        raise CustomException(msg="用户已被冻结！", code=status.HTTP_403_FORBIDDEN)
    elif user.is_cancel:
        raise CustomException(msg="用户已被注销！", code=status.HTTP_403_FORBIDDEN)
    return Auth(user=user, db=db)


class AdminAuth(BaseModel):
    admin: models.VadminUser
    db: AsyncSession

    class Config:
        arbitrary_types_allowed = True


async def full_admin(token: str = Depends(settings.oauth2_scheme), db: AsyncSession = Depends(db_getter)):
    """
    更新 full_user 以接收 JWT 令牌。

    解码接收到的令牌，对其进行校验，然后返回当前用户。

    如果令牌无效，立即返回一个 HTTP 错误。
    """
    if not token:
        raise CustomException(msg="请先登录！", code=status.HTTP_403_FORBIDDEN)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        telephone: str = payload.get("sub")
        if telephone is None:
            raise CustomException(msg="无效 Token！", code=status.HTTP_403_FORBIDDEN)
    except JWTError:
        raise CustomException(msg="无效 Token！", code=status.HTTP_403_FORBIDDEN)
    admin = await crud.UserDal(db).get_data(telephone=telephone, return_none=True,
                                            options=[models.VadminUser.roles, "roles.menus"])
    if admin is None:
        raise CustomException(msg="用户不存在！", code=status.HTTP_404_NOT_FOUND)
    elif not admin.is_active:
        raise CustomException(msg="用户已被冻结！", code=status.HTTP_403_FORBIDDEN)
    elif admin.is_cancel:
        raise CustomException(msg="用户已被注销！", code=status.HTTP_403_FORBIDDEN)
    return AdminAuth(admin=admin, db=db)