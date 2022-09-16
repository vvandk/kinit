#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : operation.py
# @IDE            : PyCharm
# @desc           : 操作记录模型


from sqlalchemy.ext.asyncio import AsyncSession
from user_agents import parse
from apps.vadmin.auth import models
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, TEXT, ForeignKey
from fastapi import Request


class VadminOperationRecord(BaseModel):
    __tablename__ = "vadmin_record_operation"
    __table_args__ = ({'comment': '操作记录表'})

    user = Column(ForeignKey("vadmin_auth_user.id", ondelete='CASCADE'), comment="操作人")
    status = Column(Boolean, default=True, comment="操作结果状态")
    ip = Column(String(50), comment="登陆地址")
    address = Column(String(50), comment="登陆地点")
    browser = Column(String(50), comment="浏览器")
    system = Column(String(50), comment="操作系统")
    response = Column(TEXT, comment="响应信息")
    request = Column(TEXT, comment="请求信息")
    request_api = Column(String(255), comment="请求接口")
    request_method = Column(String(255), comment="请求方式")

    @classmethod
    async def create_operation_record(cls, user: models.VadminUser, status: bool, request: Request, response: str,
                                      db: AsyncSession):
        """
        创建操作记录
        :return:
        """
        user_agent = parse(request.headers.get("user-agent"))
        system = f"{user_agent.os.family} {user_agent.os.version_string}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        obj = VadminOperationRecord(user=user, status=status, ip=request.client.host, browser=browser, system=system,
                                    response=response, request=str(request.__dict__), request_method=request.method,
                                    request_api=request.url)
        db.add(obj)
        await db.flush()
