#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : settings.py
# @IDE            : PyCharm
# @desc           : 系统字典模型
from sqlalchemy.orm import relationship

from db.db_base import BaseModel
from sqlalchemy import Column, String, TEXT, Integer, ForeignKey


class VadminSystemSettings(BaseModel):
    __tablename__ = "vadmin_system_settings"
    __table_args__ = ({'comment': '系统配置表'})

    config_label = Column(String(255), comment="配置表标签")
    config_key = Column(String(255), index=True, nullable=False, unique=True, comment="配置表键")
    config_value = Column(TEXT, comment="配置表内容")
    remark = Column(String(255), comment="备注信息")

    tab_id = Column(Integer, ForeignKey("vadmin_system_settings_tab.id", ondelete='CASCADE'), comment="关联tab标签")
    tab = relationship("VadminSystemSettingsTab", foreign_keys=tab_id, back_populates="settings")
