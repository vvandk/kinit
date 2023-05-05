#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : settings_tab.py
# @IDE            : PyCharm
# @desc           : 系统配置分类模型

from sqlalchemy.orm import relationship
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean


class VadminSystemSettingsTab(BaseModel):
    __tablename__ = "vadmin_system_settings_tab"
    __table_args__ = ({'comment': '系统配置分类表'})

    title = Column(String(255), comment="标题")
    classify = Column(String(255), index=True, nullable=False, comment="分类键")
    tab_label = Column(String(255), comment="tab标题")
    tab_name = Column(String(255), index=True, nullable=False, unique=True, comment="tab标识符")
    hidden = Column(Boolean, default=False, comment="是否隐藏")
    disabled = Column(Boolean, default=False, comment="是否禁用")

    settings = relationship("VadminSystemSettings", back_populates="tab")
