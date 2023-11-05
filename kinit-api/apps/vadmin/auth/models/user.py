#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : user.py
# @IDE            : PyCharm
# @desc           : 用户模型

from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, DateTime
from passlib.context import CryptContext
from .role import VadminRole
from .m2m import vadmin_auth_user_roles

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class VadminUser(BaseModel):
    __tablename__ = "vadmin_auth_user"
    __table_args__ = ({'comment': '用户表'})

    avatar: Mapped[str | None] = mapped_column(String(500), comment='头像')
    telephone: Mapped[str] = mapped_column(String(11), nullable=False, index=True, comment="手机号", unique=False)
    email: Mapped[str | None] = mapped_column(String(50), comment="邮箱地址")
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="姓名")
    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="昵称")
    password: Mapped[str] = mapped_column(String(255), nullable=True, comment="密码")
    gender: Mapped[str | None] = mapped_column(String(8), nullable=True, comment="性别")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否可用")
    is_reset_password: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="是否已经重置密码，没有重置的，登陆系统后必须重置密码"
    )
    last_ip: Mapped[str | None] = mapped_column(String(50), comment="最后一次登录IP")
    last_login: Mapped[datetime | None] = mapped_column(DateTime, comment="最近一次登录时间")
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否为工作人员")
    wx_server_openid: Mapped[str | None] = mapped_column(String(255), comment="服务端微信平台openid")
    is_wx_server_openid: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否已有服务端微信平台openid")

    roles: Mapped[set[VadminRole]] = relationship(secondary=vadmin_auth_user_roles)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        生成哈希密码
        :param password: 原始密码
        :return: 哈希密码
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        验证原始密码是否与哈希密码一致
        :param password: 原始密码
        :param hashed_password: 哈希密码
        :return:
        """
        return pwd_context.verify(password, hashed_password)

    def is_admin(self) -> bool:
        """
        获取该用户是否拥有最高权限
        以最高权限为准
        :return:
        """
        return any([i.is_admin for i in self.roles])
