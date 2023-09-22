#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据库 增删改查操作

import json
import os
from enum import Enum
from typing import Any
from redis.asyncio import Redis
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from application.settings import STATIC_ROOT, SUBSCRIBE, REDIS_DB_ENABLE
from core.database import redis_getter
from core.mongo_manage import MongoManage
from utils.file.file_manage import FileManage
from . import models, schemas
from core.crud import DalBase
from core.exception import CustomException
from utils import status
from fastapi import Request


class DictTypeDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DictTypeDal, self).__init__(db, models.VadminDictType, schemas.DictTypeSimpleOut)

    async def get_dicts_details(self, dict_types: list[str]) -> dict:
        """
        获取多个字典类型下的字典元素列表
        """
        data = {}
        options = [joinedload(self.model.details)]
        objs = await DictTypeDal(self.db).get_datas(
            limit=0,
            v_return_objs=True,
            v_options=options,
            dict_type=("in", dict_types)
        )
        for obj in objs:
            if not obj:
                data[obj.dict_type] = []
                continue
            else:
                data[obj.dict_type] = [schemas.DictDetailsSimpleOut.model_validate(i).model_dump() for i in obj.details]
        return data

    async def get_select_datas(self) -> list:
        """获取选择数据，全部数据"""
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        return [schemas.DictTypeOptionsOut.model_validate(i).model_dump() for i in queryset.scalars().all()]


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
        datas = await self.get_datas(limit=0, tab_id=tab_id, v_return_objs=True)
        result = {}
        for data in datas:
            if not data.disabled:
                result[data.config_key] = data.config_value
        return result

    async def update_datas(self, datas: dict, request: Request) -> None:
        """
        更新系统配置信息

        更新ico图标步骤：先将文件上传到本地，然后点击提交后，获取到文件地址，将上传的新文件覆盖原有文件
        原因：ico图标的路径是在前端的index.html中固定的，所以目前只能改变图片，不改变路径
        """
        for key, value in datas.items():
            if key == "web_ico":
                continue
            elif key == "web_ico_local_path":
                if not value:
                    continue
                ico = await self.get_data(config_key="web_ico", tab_id=1)
                web_ico = datas.get("web_ico")
                if ico.config_value == web_ico:
                    continue
                # 将上传的ico路径替换到static/system/favicon.ico文件
                await FileManage.async_copy(value, os.path.join(STATIC_ROOT, "system/favicon.ico"))
                sql = update(self.model).where(self.model.config_key == "web_ico").values(config_value=web_ico)
                await self.db.execute(sql)
            else:
                sql = update(self.model).where(self.model.config_key == str(key)).values(config_value=value)
                await self.db.execute(sql)
        if "wx_server_app_id" in datas and REDIS_DB_ENABLE:
            rd = redis_getter(request)
            await rd.client().set("wx_server", json.dumps(datas))

    async def get_base_config(self) -> dict:
        """
        获取系统基本信息
        """
        ignore_configs = ["wx_server_app_id", "wx_server_app_secret"]
        datas = await self.get_datas(limit=0, tab_id=("in", ["1", "9"]), disabled=False, v_return_objs=True)
        result = {}
        for config in datas:
            if config.config_key not in ignore_configs:
                result[config.config_key] = config.config_value
        return result


class SettingsTabDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SettingsTabDal, self).__init__(db, models.VadminSystemSettingsTab, schemas.SettingsTabSimpleOut)

    async def get_classify_tab_values(self, classify: list[str], hidden: bool | None = False) -> dict:
        """
        获取系统配置分类下的标签信息
        """
        model = models.VadminSystemSettingsTab
        options = [joinedload(model.settings)]
        datas = await self.get_datas(
            limit=0,
            v_options=options,
            classify=("in", classify),
            disabled=False,
            v_return_objs=True,
            hidden=hidden
        )
        return self.__generate_values(datas)

    async def get_tab_name_values(self, tab_names: list[str], hidden: bool | None = False) -> dict:
        """
        获取系统配置标签下的标签信息
        """
        model = models.VadminSystemSettingsTab
        options = [joinedload(model.settings)]
        datas = await self.get_datas(
            limit=0,
            v_options=options,
            tab_name=("in", tab_names),
            disabled=False,
            v_return_objs=True,
            hidden=hidden
        )
        return self.__generate_values(datas)

    @classmethod
    def __generate_values(cls, datas: list[models.VadminSystemSettingsTab]) -> dict:
        """
        生成字典值
        """
        return {
            tab.tab_name: {
                item.config_key: item.config_value
                for item in tab.settings
                if not item.disabled
            }
            for tab in datas
        }


class TaskDal(MongoManage):

    class JobOperation(Enum):
        add = "add_job"

    def __init__(self, db: AsyncIOMotorDatabase):
        super(TaskDal, self).__init__(db, "vadmin_system_task", schemas.TaskSimpleOut)

    async def get_task(
            self,
            _id: str = None,
            v_return_none: bool = False,
            v_schema: Any = None,
            **kwargs
    ) -> dict | None:
        """
        获取单个数据，默认使用 ID 查询，否则使用关键词查询

        包括临时字段 last_run_datetime，is_active
        is_active: 只有在 scheduler_task_jobs 任务运行表中存在相同 _id 才表示任务添加成功，任务状态才为 True
        last_run_datetime: 在 scheduler_task_record 中获取该任务最近一次执行完成的时间

        :param _id: 数据 ID
        :param v_return_none: 是否返回空 None，否则抛出异常，默认抛出异常
        :param v_schema: 指定使用的序列化对象
        """
        if _id:
            kwargs["_id"] = ("ObjectId", _id)

        params = self.filter_condition(**kwargs)
        pipeline = [
            {
                '$addFields': {
                    'str_id': {'$toString': '$_id'}
                }
            },
            {
                '$lookup': {
                    'from': 'scheduler_task_jobs',
                    'localField': 'str_id',
                    'foreignField': '_id',
                    'as': 'matched_jobs'
                }
            },
            {
                '$lookup': {
                    'from': 'scheduler_task_record',
                    'localField': 'str_id',
                    'foreignField': 'job_id',
                    'as': 'matched_records'
                }
            },
            {
                '$addFields': {
                    'is_active': {
                        '$cond': {
                            'if': {'$ne': ['$matched_jobs', []]},
                            'then': True,
                            'else': False
                        }
                    },
                    'last_run_datetime': {
                        '$ifNull': [
                            {'$arrayElemAt': ['$matched_records.create_datetime', -1]},
                            None
                        ]
                    }
                }
            },
            {
                '$project': {
                    'matched_records': 0,
                    'matched_jobs': 0
                }
            },
            {
                '$match': params
            },
            {
                '$facet': {
                    'documents': [
                        {'$limit': 1},
                    ]
                }
            }
        ]
        # 执行聚合查询
        cursor = self.collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)
        data = result[0]['documents']
        if not data and v_return_none:
            return None
        elif not data:
            raise CustomException("未查找到对应数据", code=status.HTTP_404_NOT_FOUND)
        data = data[0]
        if data and v_schema:
            return jsonable_encoder(v_schema(**data))
        return data

    async def get_tasks(
            self,
            page: int = 1,
            limit: int = 10,
            v_schema: Any = None,
            v_order: str = None,
            v_order_field: str = None,
            **kwargs
    ) -> tuple:
        """
        获取任务信息列表

        添加了两个临时字段
        is_active: 只有在 scheduler_task_jobs 任务运行表中存在相同 _id 才表示任务添加成功，任务状态才为 True
        last_run_datetime: 在 scheduler_task_record 中获取该任务最近一次执行完成的时间
        """
        v_order_field = v_order_field if v_order_field else 'create_datetime'
        v_order = -1 if v_order in self.ORDER_FIELD else 1
        params = self.filter_condition(**kwargs)
        pipeline = [
            {
                '$addFields': {
                    'str_id': {'$toString': '$_id'}
                }
            },
            {
                '$lookup': {
                    'from': 'scheduler_task_jobs',
                    'localField': 'str_id',
                    'foreignField': '_id',
                    'as': 'matched_jobs'
                }
            },
            {
                '$lookup': {
                    'from': 'scheduler_task_record',
                    'localField': 'str_id',
                    'foreignField': 'job_id',
                    'as': 'matched_records'
                }
            },
            {
                '$addFields': {
                    'is_active': {
                        '$cond': {
                            'if': {'$ne': ['$matched_jobs', []]},
                            'then': True,
                            'else': False
                        }
                    },
                    'last_run_datetime': {
                        '$ifNull': [
                            {'$arrayElemAt': ['$matched_records.create_datetime', -1]},
                            None
                        ]
                    }
                }
            },
            {
                '$project': {
                    'matched_records': 0,
                    'matched_jobs': 0
                }
            },
            {
                '$match': params
            },
            {
                '$facet': {
                    'documents': [
                        {'$sort': {v_order_field: v_order}},
                        {'$limit': limit},
                        {'$skip': (page - 1) * limit}
                    ],
                    'count': [{'$count': 'total'}]
                }
            }
        ]

        # 执行聚合查询
        cursor = self.collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)
        datas = result[0]['documents']
        count = result[0]['count'][0]['total'] if result[0]['count'] else 0
        if count == 0:
            return [], 0
        elif v_schema:
            datas = [jsonable_encoder(v_schema(**data)) for data in datas]
        elif self.schema:
            datas = [jsonable_encoder(self.schema(**data)) for data in datas]
        return datas, count

    async def add_task(self, rd: Redis, data: dict) -> int:
        """
        添加任务到消息队列

        使用消息无保留策略：无保留是指当发送者向某个频道发送消息时，如果没有订阅该频道的调用方，就直接将该消息丢弃。

        :params rd: redis 对象
        :params data: 行数据字典
        :return: 接收到消息的订阅者数量。
        """
        exec_strategy = data.get("exec_strategy")
        job_params = {
            "name": data.get("_id"),
            "job_class": data.get("job_class"),
            "expression": data.get("expression")
        }
        if exec_strategy == "interval" or exec_strategy == "cron":
            job_params["start_date"] = data.get("start_date")
            job_params["end_date"] = data.get("end_date")
        message = {
            "operation": self.JobOperation.add.value,
            "task": {
                "exec_strategy": data.get("exec_strategy"),
                "job_params": job_params
            }
        }
        return await rd.publish(SUBSCRIBE, json.dumps(message).encode('utf-8'))

    async def create_task(self, rd: Redis, data: schemas.Task) -> dict:
        """
        创建任务
        """
        data_dict = data.model_dump()
        is_active = data_dict.pop('is_active')
        insert_result = await super().create_data(data_dict)
        obj = await self.get_task(insert_result.inserted_id, v_schema=schemas.TaskSimpleOut)

        # 如果分组不存在则新增分组
        group = await TaskGroupDal(self.db).get_data(value=data.group, v_return_none=True)
        if not group:
            await TaskGroupDal(self.db).create_data({"value": data.group})

        result = {
            "subscribe_number": 0,
            "is_active": is_active
        }

        if is_active:
            # 创建任务成功后, 如果任务状态为 True，则向消息队列中发送任务
            result['subscribe_number'] = await self.add_task(rd, obj)
        return result

    async def put_task(self, rd: Redis, _id: str, data: schemas.Task) -> dict:
        """
        更新任务
        """
        data_dict = data.model_dump()
        is_active = data_dict.pop('is_active')
        await super(TaskDal, self).put_data(_id, data)
        obj: dict = await self.get_task(_id, v_schema=schemas.TaskSimpleOut)

        # 如果分组不存在则新增分组
        group = await TaskGroupDal(self.db).get_data(value=data.group, v_return_none=True)
        if not group:
            await TaskGroupDal(self.db).create_data({"value": data.group})

        try:
            # 删除正在运行中的 Job
            await SchedulerTaskJobsDal(self.db).delete_data(_id)
        except CustomException as e:
            pass

        result = {
            "subscribe_number": 0,
            "is_active": is_active
        }

        if is_active:
            # 更新任务成功后, 如果任务状态为 True，则向消息队列中发送任务
            result['subscribe_number'] = await self.add_task(rd, obj)
        return result

    async def delete_task(self, _id: str) -> bool:
        """
        删除任务
        """
        result = await super(TaskDal, self).delete_data(_id)

        try:
            # 删除正在运行中的 Job
            await SchedulerTaskJobsDal(self.db).delete_data(_id)
        except CustomException as e:
            pass
        return result

    async def run_once_task(self, rd: Redis, _id: str) -> int:
        """
        执行一次任务
        """
        obj: dict = await self.get_data(_id, v_schema=schemas.TaskSimpleOut)
        message = {
            "operation": self.JobOperation.add.value,
            "task": {
                "exec_strategy": "once",
                "job_params": {
                    "name": obj.get("_id"),
                    "job_class": obj.get("job_class")
                }
            }
        }
        return await rd.publish(SUBSCRIBE, json.dumps(message).encode('utf-8'))


class TaskGroupDal(MongoManage):

    def __init__(self, db: AsyncIOMotorDatabase):
        super(TaskGroupDal, self).__init__(db, "vadmin_system_task_group")


class TaskRecordDal(MongoManage):

    def __init__(self, db: AsyncIOMotorDatabase):
        super(TaskRecordDal, self).__init__(db, "scheduler_task_record")


class SchedulerTaskJobsDal(MongoManage):

    def __init__(self, db: AsyncIOMotorDatabase):
        super(SchedulerTaskJobsDal, self).__init__(db, "scheduler_task_jobs", is_object_id=False)
