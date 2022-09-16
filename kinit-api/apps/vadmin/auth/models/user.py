#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : user.py
# @IDE            : PyCharm
# @desc           : 用户模型

import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime
from passlib.context import CryptContext
from .m2m import vadmin_user_roles

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class VadminUser(BaseModel):
    __tablename__ = "vadmin_auth_user"
    __table_args__ = ({'comment': '用户表'})

    avatar = Column(String(500), nullable=True, comment='头像')
    telephone = Column(String(11), nullable=False, index=True, comment="手机号", unique=True)
    name = Column(String(50), index=True, nullable=False, comment="姓名")
    nickname = Column(String(50), nullable=True, comment="昵称")
    password = Column(String(255), nullable=True, comment="密码")
    gender = Column(String(8), nullable=True, comment="性别")
    is_active = Column(Boolean, default=True, comment="是否可用")
    is_cancel = Column(Boolean, default=False, comment="是否注销")
    is_reset_password = Column(Boolean, default=False, comment="是否已经重置密码，没有重置的，登陆系统后必须重置密码")
    last_ip = Column(String(50), nullable=True, comment="最后一次登录IP")
    last_login = Column(DateTime, nullable=True, comment="最近一次登录时间")

    roles = relationship("VadminRole", back_populates='users', secondary=vadmin_user_roles)

    # generate hash password
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    # verify login password
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    async def update_login_info(self, db: AsyncSession, last_ip: str):
        """
        更新当前登录信息
        :param db: 数据库
        :param last_ip: 最近一次登录 IP
        :return:
        """
        self.last_ip = last_ip
        self.last_login = datetime.datetime.now()
        await db.flush()

    async def is_admin(self) -> bool:
        """
        获取该用户是否拥有最高权限

        以最高权限为准

        :return:
        """
        return any([i.is_admin for i in self.roles])
