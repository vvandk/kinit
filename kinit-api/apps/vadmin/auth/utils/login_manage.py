#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/8/8 11:02
# @File           : auth_util.py
# @IDE            : PyCharm
# @desc           : 简要说明

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request
from application import settings
from jose import jwt
from apps.vadmin.auth import models
from .validation import LoginValidation, LoginForm, LoginResult
from utils.aliyun_sms import AliyunSMS


class LoginManage:
    """
    登录认证工具
    """

    @LoginValidation
    async def password_login(self, data: LoginForm, user: models.VadminUser, **kwargs) -> LoginResult:
        """
        验证用户密码
        """
        result = models.VadminUser.verify_password(data.password, user.password)
        if result:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="手机号或密码错误")

    @LoginValidation
    async def sms_login(self, data: LoginForm, request: Request, **kwargs) -> LoginResult:
        """
        验证用户短信验证码
        """
        rd = request.app.state.redis
        sms = AliyunSMS(rd, data.telephone)
        result = await sms.check_sms_code(data.password)
        if result:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="验证码错误")

    @staticmethod
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
