#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/7/7 13:41
# @File           : user.py
# @IDE            : PyCharm
# @desc           : 系统字典模型

from sqlalchemy.orm import relationship
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer


class VadminDictType(BaseModel):
    __tablename__ = "vadmin_system_dict_type"
    __table_args__ = ({'comment': '字典类型表'})

    dict_name = Column(String(50), index=True, nullable=False, comment="字典名称")
    dict_type = Column(String(50), index=True, nullable=False, comment="字典类型")
    disabled = Column(Boolean, default=False, comment="字典状态，是否禁用")
    remark = Column(String(255), comment="备注")
    details = relationship("VadminDictDetails", back_populates="dict_type")


class VadminDictDetails(BaseModel):
    __tablename__ = "vadmin_system_dict_details"
    __table_args__ = ({'comment': '字典详情表'})

    label = Column(String(50), index=True, nullable=False, comment="字典标签")
    value = Column(String(50), index=True, nullable=False, comment="字典键值")
    disabled = Column(Boolean, default=False, comment="字典状态，是否禁用")
    is_default = Column(Boolean, default=False, comment="是否默认")
    order = Column(Integer, comment="字典排序")
    dict_type_id = Column(Integer, ForeignKey("vadmin_system_dict_type.id", ondelete='CASCADE'), comment="关联字典类型")
    dict_type = relationship("VadminDictType", foreign_keys=dict_type_id, back_populates="details")
    remark = Column(String(255), comment="备注")
