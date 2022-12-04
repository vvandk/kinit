#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/18 22:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据库 增删改查操作

# sqlalchemy 查询操作：https://segmentfault.com/a/1190000016767008
# sqlalchemy 增删改操作：https://www.osgeo.cn/sqlalchemy/tutorial/orm_data_manipulation.html#updating-orm-objects
# SQLAlchemy lazy load和eager load: https://www.jianshu.com/p/dfad7c08c57a
# Mysql中内连接,左连接和右连接的区别总结:https://www.cnblogs.com/restartyang/articles/9080993.html
# SQLAlchemy join 内连接
# selectinload 官方文档：
# https://www.osgeo.cn/sqlalchemy/orm/loading_relationships.html?highlight=selectinload#sqlalchemy.orm.selectinload
import datetime
from typing import List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, delete, update, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status
from core.logger import logger
from sqlalchemy.sql.selectable import Select


class DalBase:

    def __init__(self, db: AsyncSession, model, schema, key_models: dict = None):
        self.db = db
        self.model = model
        self.schema = schema
        self.key_models = key_models

    async def get_data(self, data_id: int = None, options: list = None, schema=None, keys: dict = None, **kwargs):
        """
        获取单个数据，默认使用 ID 查询，否则使用关键词查询

        @param data_id:
        @param keys: 外键字段查询，内连接
        @param options: 指示应使用select在预加载中加载给定的属性。
        @param schema: 指定使用的序列化对象
        @param kwargs: 关键词参数,
        @param kwargs: v_order，排序，默认正序，为 desc 是倒叙
        @param kwargs: v_return_none，是否返回空 None，否认 抛出异常，默认抛出异常
        """
        order = kwargs.pop("v_order", None)
        return_none = kwargs.pop("v_return_none", False)
        keys_exist = False
        if keys:
            for key, value in keys.items():
                if value and isinstance(value, dict):
                    for k, v in value.items():
                        if v:
                            keys_exist = True
                            break
        kwargs_exist = False
        if kwargs:
            for key, value in kwargs.items():
                if value and getattr(self.model, key, None):
                    kwargs_exist = True
                    break
        sql = select(self.model).where(self.model.delete_datetime.is_(None))
        if data_id or kwargs_exist or keys_exist:
            if data_id:
                sql = sql.where(self.model.id == data_id)
            sql = self.add_filter_condition(sql, keys, options, **kwargs)
        if order and (order == "desc" or order == "descending"):
            sql = sql.order_by(self.model.create_datetime.desc())
        queryset = await self.db.execute(sql)
        data = queryset.scalars().first()
        if not data and return_none:
            return None
        if data and schema:
            return schema.from_orm(data).dict()
        if data:
            return data
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到此数据")

    async def get_datas(self, page: int = 1, limit: int = 10, keys: dict = None, options: list = None, schema=None,
                        **kwargs):
        """
        获取数据列表

        @param page: 页码
        @param limit: 当前页数据量
        @param keys: 外键字段查询
        @param options: 指示应使用select在预加载中加载给定的属性。
        @param schema: 指定使用的序列化对象
        @param kwargs: v_order，排序，默认正序，为 desc 是倒叙
        @param kwargs: v_order_field，排序字段
        @param kwargs: v_return_objs，是否返回对象
        @param kwargs: v_start_sql，初始 sql
        """
        order = kwargs.pop("v_order", None)
        order_field = kwargs.pop("v_order_field", None)
        return_objs = kwargs.pop("v_return_objs", False)
        start_sql = kwargs.pop("v_start_sql", None)
        if not isinstance(start_sql, Select):
            start_sql = select(self.model).where(self.model.delete_datetime.is_(None))
        sql = self.add_filter_condition(start_sql, keys, options, **kwargs)
        if order_field and (order == "desc" or order == "descending"):
            sql = sql.order_by(getattr(self.model, order_field).desc(), self.model.id.desc())
        elif order_field:
            sql = sql.order_by(getattr(self.model, order_field), self.model.id)
        elif order == "desc" or order == "descending":
            sql = sql.order_by(self.model.id.desc())
        if limit != 0:
            sql = sql.offset((page - 1) * limit).limit(limit)
        queryset = await self.db.execute(sql)
        if return_objs:
            return queryset.scalars().all()
        if schema:
            return [schema.from_orm(i).dict() for i in queryset.scalars().all()]
        return [self.out_dict(i) for i in queryset.scalars().all()]

    async def get_count(self, keys: dict = None, **kwargs):
        """获取数据总数"""
        sql = select(func.count(self.model.id).label('total')).where(self.model.delete_datetime.is_(None))
        sql = self.add_filter_condition(sql, keys, **kwargs)
        queryset = await self.db.execute(sql)
        return queryset.one()['total']

    async def create_data(self, data, return_obj: bool = False, options: list = None, schema=None):
        """创建数据"""
        if isinstance(data, dict):
            obj = self.model(**data)
        else:
            obj = self.model(**data.dict())
        await self.flush(obj)
        if options:
            obj = await self.get_data(obj.id, options=options)
        if return_obj:
            return obj
        if schema:
            return schema.from_orm(obj).dict()
        return self.out_dict(obj)

    async def put_data(self, data_id: int, data, return_obj: bool = False, options: list = None, schema=None):
        """
        更新单个数据
        """
        obj = await self.get_data(data_id, options=options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        if return_obj:
            return obj
        if schema:
            return schema.from_orm(obj).dict()
        return self.out_dict(obj)

    async def delete_datas(self, ids: List[int], soft: bool = False):
        """
        删除多条数据
        @param ids: 数据集
        @param soft: 是否执行软删除
        """
        if soft:
            await self.db.execute(update(self.model).where(self.model.id.in_(ids)).
                                  values(delete_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            await self.db.execute(delete(self.model).where(self.model.id.in_(ids)))

    def add_filter_condition(self, sql: select, keys: dict = None, options: list = None, **kwargs) -> select:
        """
        添加过滤条件，以及内连接过滤条件
        @param sql:
        @param keys: 外键字段查询，内连接
        @param options: 指示应使用select在预加载中加载给定的属性。
        @param kwargs: 关键词参数
        """
        if keys and self.key_models:
            for key, value in keys.items():
                model = self.key_models.get(key)
                if model:
                    sql = sql.join(model)
                    for v_key, v_value in value.items():
                        if v_value is not None and v_value != "":
                            v_attr = getattr(model, v_key, None)
                            sql = self.filter_condition(sql, v_attr, v_value)
                else:
                    logger.error(f"外键查询报错：{key}模型不存在，无法进行下一步查询。")
        elif keys and not self.key_models:
            logger.error(f"外键查询报错：key_models 外键模型无配置项，无法进行下一步查询。")
        for field in kwargs:
            value = kwargs.get(field)
            if value is not None and value != "":
                attr = getattr(self.model, field, None)
                sql = self.filter_condition(sql, attr, value)
        if options:
            sql = sql.options(*[selectinload(i) for i in options])
        return sql

    @classmethod
    def filter_condition(cls, sql, attr, value):
        """
        过滤条件
        """
        if not attr:
            return sql
        if isinstance(value, tuple):
            if value[0] == "date" and value[1]:
                # 根据日期查询， 关键函数是：func.time_format和func.date_format
                sql = sql.where(func.date_format(attr, "%Y-%m-%d") == value[1])
            elif value[0] == "like" and value[1]:
                sql = sql.where(attr.like(f"%{value[1]}%"))
            elif value[0] == "or" and value[1]:
                sql = sql.where(or_(i for i in value[1]))
            elif value[0] == "in" and value[1]:
                sql = sql.where(attr.in_(value[1]))
            elif value[0] == "between" and value[1]:
                sql = sql.where(attr.between(value[1][0], value[1][1]))
            elif value[0] == "month" and value[1]:
                sql = sql.where(func.date_format(attr, "%Y-%m") == value[1])
        else:
            sql = sql.where(attr == value)
        return sql

    async def flush(self, obj=None):
        """
        刷新到数据库
        """
        if obj:
            self.db.add(obj)
        await self.db.flush()
        if obj:
            await self.db.refresh(obj)

    def out_dict(self, data):
        """
        序列化
        @param data:
        @return:
        """
        return self.schema.from_orm(data).dict()
