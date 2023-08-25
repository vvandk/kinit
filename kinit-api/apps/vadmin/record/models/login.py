#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : login.py
# @IDE            : PyCharm
# @desc           : 登录记录模型
import json

from sqlalchemy.orm import Mapped, mapped_column

from application.settings import LOGIN_LOG_RECORD
from apps.vadmin.auth.utils.validation import LoginForm, WXLoginForm
from utils.ip_manage import IPManage
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Text
from fastapi import Request
from starlette.requests import Request as StarletteRequest
from user_agents import parse


class VadminLoginRecord(BaseModel):
    __tablename__ = "vadmin_record_login"
    __table_args__ = ({'comment': '登录记录表'})

    telephone: Mapped[str] = mapped_column(String(255), index=True, nullable=False, comment="手机号")
    status: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否登录成功")
    platform: Mapped[str] = mapped_column(String(8), comment="登陆平台")
    login_method: Mapped[str] = mapped_column(String(8), comment="认证方式")
    ip: Mapped[str | None] = mapped_column(String(50), comment="登陆地址")
    address: Mapped[str | None] = mapped_column(String(255), comment="登陆地点")
    country: Mapped[str | None] = mapped_column(String(255), comment="国家")
    province: Mapped[str | None] = mapped_column(String(255), comment="县")
    city: Mapped[str | None] = mapped_column(String(255), comment="城市")
    county: Mapped[str | None] = mapped_column(String(255), comment="区/县")
    operator: Mapped[str | None] = mapped_column(String(255), comment="运营商")
    postal_code: Mapped[str | None] = mapped_column(String(255), comment="邮政编码")
    area_code: Mapped[str | None] = mapped_column(String(255), comment="地区区号")
    browser: Mapped[str | None] = mapped_column(String(50), comment="浏览器")
    system: Mapped[str | None] = mapped_column(String(50), comment="操作系统")
    response: Mapped[str | None] = mapped_column(Text, comment="响应信息")
    request: Mapped[str | None] = mapped_column(Text, comment="请求信息")

    @classmethod
    async def create_login_record(
            cls,
            db: AsyncSession,
            data: LoginForm | WXLoginForm,
            status: bool,
            req: Request | StarletteRequest,
            resp: dict
    ):
        """
        创建登录记录
        :return:
        """
        if not LOGIN_LOG_RECORD:
            return None
        header = {}
        for k, v in req.headers.items():
            header[k] = v
        if isinstance(req, StarletteRequest):
            form = (await req.form()).multi_items()
            params = json.dumps({"form": form, "headers": header})
        else:
            body = json.loads((await req.body()).decode())
            params = json.dumps({"body": body, "headers": header})
        user_agent = parse(req.headers.get("user-agent"))
        system = f"{user_agent.os.family} {user_agent.os.version_string}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        ip = IPManage(req.client.host)
        location = await ip.parse()
        obj = VadminLoginRecord(
            **location.dict(),
            telephone=data.telephone if data.telephone else data.code,
            status=status,
            browser=browser,
            system=system,
            response=json.dumps(resp),
            request=params,
            platform=data.platform,
            login_method=data.method
        )
        db.add(obj)
        await db.flush()
