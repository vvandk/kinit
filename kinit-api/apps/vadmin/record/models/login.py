#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : login.py
# @IDE            : PyCharm
# @desc           : 登录记录模型


from sqlalchemy.ext.asyncio import AsyncSession
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, TEXT
from fastapi import Request
from user_agents import parse


class VadminLoginRecord(BaseModel):
    __tablename__ = "vadmin_record_login"
    __table_args__ = ({'comment': '登录记录表'})

    telephone = Column(String(50), index=True, nullable=False, comment="手机号")
    status = Column(Boolean, default=True, comment="是否登录成功")
    ip = Column(String(50), comment="登陆地址")
    address = Column(String(50), comment="登陆地点")
    browser = Column(String(50), comment="浏览器")
    system = Column(String(50), comment="操作系统")
    response = Column(TEXT, comment="响应信息")
    request = Column(TEXT, comment="请求信息")

    @classmethod
    async def create_login_record(cls, telephone: str, status: bool, request: Request, response: str
                                  , db: AsyncSession):
        """
        创建登录记录
        :return:
        """
        user_agent = parse(request.headers.get("user-agent"))
        system = f"{user_agent.os.family} {user_agent.os.version_string}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        obj = VadminLoginRecord(telephone=telephone, status=status, ip=request.client.host, browser=browser,
                                system=system, response=response, request=str(request.__dict__))
        db.add(obj)
        await db.flush()
