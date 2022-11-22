#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/11/9 10:15 
# @File           : login.py
# @IDE            : PyCharm
# @desc           : 登录验证装饰器

from fastapi import Request, Depends
from pydantic import BaseModel, validator
from sqlalchemy.ext.asyncio import AsyncSession
from apps.vadmin.auth import models, crud, schemas
from core.database import db_getter
from core.validator import vali_telephone
from typing import Optional


class LoginForm(BaseModel):
    telephone: str
    password: str
    method: str = '0'  # 认证方式，0：密码登录，1：短信登录

    # validators
    _normalize_telephone = validator('telephone', allow_reuse=True)(vali_telephone)


class LoginResult(BaseModel):
    status: Optional[bool] = False
    user: Optional[schemas.UserOut] = None
    msg: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class LoginValidation:

    """
    验证用户登录时提交的数据是否有效
    """

    def __init__(self, func):
        self.func = func

    async def __call__(self, data: LoginForm, db: AsyncSession, request: Request) -> LoginResult:
        self.result = LoginResult()
        options = [models.VadminUser.roles, "roles.menus"]
        user = await crud.UserDal(db).get_data(telephone=data.telephone, v_return_none=True, options=options)
        if not user:
            self.result.msg = "该手机号不存在！"
            return self.result

        result = await self.func(self, data=data, user=user, request=request)

        if not result.status:
            self.result.msg = result.msg
        elif not user.is_active:
            self.result.msg = "此手机号已被冻结！"
        elif user.is_cancel:
            self.result.msg = "此手机号已被注销！"
        elif user:
            self.result.msg = "OK"
            self.result.status = True
            self.result.user = schemas.UserOut.from_orm(user)
            await user.update_login_info(db, request.client.host)
        return self.result
