#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/8/8 11:02
# @File           : auth_util.py
# @IDE            : PyCharm
# @desc           : 简要说明

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter
from application import settings
from jose import jwt
from apps.vadmin.auth import crud, models
from pydantic import BaseModel, validator
from core.validator import vali_telephone


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    创建一个生成新的访问令牌的工具函数。
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


class LoginForm(BaseModel):
    telephone: str
    password: str

    # validators
    _normalize_telephone = validator('telephone', allow_reuse=True)(vali_telephone)


async def authenticate_user(data: LoginForm, db: AsyncSession = Depends(db_getter)):
    """验证用户密码"""
    result = {
        "status": False,
        "user": None,
        "msg": None,
        "data": data,
        "db": db
    }
    user = await crud.UserDal(db).get_data(telephone=data.telephone, return_none=True, options=[models.VadminUser.roles])
    if not user:
        result["msg"] = "该手机号不存在！"
    elif not models.VadminUser.verify_password(data.password, user.password):
        result["msg"] = "手机号或密码不正确！"
    elif not user.is_active:
        result["msg"] = "此手机号已被冻结！"
    elif user.is_cancel:
        result["msg"] = "此手机号已被注销！"
    elif user:
        result["status"] = True
        result["user"] = user
    return result
