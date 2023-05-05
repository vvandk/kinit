#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : issue.py
# @IDE            : PyCharm
# @desc           : 常见问题

from sqlalchemy.orm import relationship
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text


class VadminIssueCategory(BaseModel):
    __tablename__ = "vadmin_help_issue_category"
    __table_args__ = ({'comment': '常见问题类别表'})

    name = Column(String(50), index=True, nullable=False, comment="类别名称")
    platform = Column(String(8), index=True, nullable=False, comment="展示平台")
    is_active = Column(Boolean, default=True, comment="是否可见")

    issues = relationship("VadminIssue", back_populates='category')

    user_id = Column(ForeignKey("vadmin_auth_user.id", ondelete='SET NULL'), comment="创建人")
    user = relationship("VadminUser", foreign_keys=user_id)


class VadminIssue(BaseModel):
    __tablename__ = "vadmin_help_issue"
    __table_args__ = ({'comment': '常见问题记录表'})

    category_id = Column(ForeignKey("vadmin_help_issue_category.id", ondelete='CASCADE'), comment="类别")
    category = relationship("VadminIssueCategory", foreign_keys=category_id, back_populates='issues')

    title = Column(String(255), index=True, nullable=False, comment="标题")
    content = Column(Text, comment="内容")
    view_number = Column(Integer, default=0, comment="查看次数")
    is_active = Column(Boolean, default=True, comment="是否可见")

    user_id = Column(ForeignKey("vadmin_auth_user.id", ondelete='SET NULL'), comment="创建人")
    user = relationship("VadminUser", foreign_keys=user_id)

