# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : current.py
# @IDE            : PyCharm
# @desc           : 获取认证后的信息工具

from sqlalchemy.ext.asyncio import AsyncSession
from apps.vadmin.auth import crud, models
from .validation import AuthValidation, Auth


async def get_user_permissions(user):
    """
    获取跟进系统用户所有权限列表
    """
    if any([role.is_admin for role in user.roles]):
        return ['*.*.*']
    permissions = set()
    for role_obj in user.roles:
        for menu in role_obj.menus:
            if menu.perms and not menu.disabled:
                permissions.add(menu.perms)
    return list(permissions)


@AuthValidation
async def login_auth(telephone: str, db: AsyncSession):
    """
    更新 login_auth 以接收 JWT 令牌。

    解码接收到的令牌，对其进行校验，然后返回当前用户。

    如果令牌无效，立即返回一个 HTTP 错误。
    """
    return await crud.UserDal(db).get_data(telephone=telephone, v_return_none=True)


@AuthValidation
async def full_admin(telephone: str, db: AsyncSession):
    """
    更新 full_user 以接收 JWT 令牌。

    解码接收到的令牌，对其进行校验，然后返回当前用户。

    如果令牌无效，立即返回一个 HTTP 错误。
    """
    options = [models.VadminUser.roles, "roles.menus"]
    return await crud.UserDal(db).get_data(telephone=telephone, v_return_none=True, options=options)

