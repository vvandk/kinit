#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据库 增删改查操作

# sqlalchemy 查询操作：https://segmentfault.com/a/1190000016767008
# sqlalchemy 关联查询：https://www.jianshu.com/p/dfad7c08c57a
# sqlalchemy 关联查询详细：https://blog.csdn.net/u012324798/article/details/103940527
from typing import List, Union
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from utils.file_manage import FileManage
from . import models, schemas
from core.crud import DalBase


class DictTypeDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DictTypeDal, self).__init__(db, models.VadminDictType, schemas.DictTypeSimpleOut)

    async def get_dicts_details(self, dict_types: List[str]) -> dict:
        """
        获取多个字典类型下的字典元素列表
        """
        data = {}
        for dict_type in dict_types:
            dict_data = await DictTypeDal(self.db).\
                get_data(dict_type=dict_type, return_none=True, options=[self.model.details])
            if not dict_data:
                data[dict_type] = []
                continue
            else:
                data[dict_type] = [schemas.DictDetailsSimpleOut.from_orm(i).dict() for i in dict_data.details]
        return data

    async def get_select_datas(self):
        """获取选择数据，全部数据"""
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        return [schemas.DictTypeSelectOut.from_orm(i).dict() for i in queryset.scalars().all()]


class DictDetailsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DictDetailsDal, self).__init__(db, models.VadminDictDetails, schemas.DictDetailsSimpleOut)


class SettingsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SettingsDal, self).__init__(db, models.VadminSystemSettings, schemas.SettingsSimpleOut)

    async def get_tab_values(self, tab_id: int) -> dict:
        """
        获取系统配置标签下的信息
        """
        datas = await self.get_datas(limit=0, tab_id=tab_id, return_objs=True)
        result = {}
        for data in datas:
            result[data.config_key] = data.config_value
        return result

    async def update_datas(self, datas: dict):
        """
        更新系统配置信息

        更新ico图标步骤：先将文件上传到本地，然后点击提交后，获取到文件地址，将上传的新文件覆盖原有文件
        原因：ico图标的路径是在前端的index.html中固定的，所以目前只能改变图片，不改变路径
        """
        for key, value in datas.items():
            if key == "web_ico":
                if not value:
                    continue
                ico = await self.get_data(config_key="web_ico", tab_id=1)
                if ico.config_value == value:
                    continue
                # 将上传的ico路径替换到static/system/favicon.ico文件
                FileManage.copy(value, "static/system/favicon.ico")
            await self.db.execute(update(self.model).where(self.model.config_key == key).values(config_value=value))


class SettingsTabDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SettingsTabDal, self).__init__(db, models.VadminSystemSettingsTab, schemas.SettingsTabSimpleOut)

    async def get_classify_tab_values(self, classify: List[str], hidden: Union[bool, None] = False):
        """
        获取系统配置分类下的所有显示标签信息
        """
        model = models.VadminSystemSettingsTab
        options = [model.settings]
        datas = await self.get_datas(limit=0, options=options, classify=("in", classify), disabled=False,
                                     return_objs=True, hidden=hidden)
        result = {}
        for tab in datas:
            tabs = {}
            for item in tab.settings:
                tabs[item.config_key] = item.config_value
            result[tab.tab_name] = tabs
        return result

