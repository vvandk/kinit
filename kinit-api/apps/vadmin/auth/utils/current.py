# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/24 16:44
# @File           : current.py
# @IDE            : PyCharm
# @desc           : 获取认证后的信息工具

from sqlalchemy.ext.asyncio import AsyncSession
from apps.vadmin.auth import crud, models
from .validation import AuthValidation, Auth


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


@AuthValidation
async def login_auth(telephone: str, db: AsyncSession):
    """
    更新 login_auth 以接收 JWT 令牌。

    解码接收到的令牌，对其进行校验，然后返回当前用户。

    如果令牌无效，立即返回一个 HTTP 错误。
    """
    return await crud.UserDal(db).get_data(telephone=telephone, return_none=True)


@AuthValidation
async def full_admin(telephone: str, db: AsyncSession):
    """
    更新 full_user 以接收 JWT 令牌。

    解码接收到的令牌，对其进行校验，然后返回当前用户。

    如果令牌无效，立即返回一个 HTTP 错误。
    """
    options = [models.VadminUser.roles, "roles.menus"]
    return await crud.UserDal(db).get_data(telephone=telephone, return_none=True, options=options)

