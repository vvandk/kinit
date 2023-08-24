#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Update Time    : 2023/8/21 22:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据库 增删改查操作

# sqlalchemy 官方文档：https://docs.sqlalchemy.org/en/20/index.html
# sqlalchemy 查询操作（官方文档）: https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
# sqlalchemy 增删改操作：https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html
# sqlalchemy 1.x 语法迁移到 2.x :https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage

import datetime
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, delete, update, BinaryExpression, ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.strategy_options import _AbstractLoad
from starlette import status
from core.exception import CustomException
from sqlalchemy.sql.selectable import Select as SelectType
from typing import Any


class DalBase:
    # 倒叙
    ORDER_FIELD = ["desc", "descending"]

    def __init__(self, db: AsyncSession, model: Any, schema: Any):
        self.db = db
        self.model = model
        self.schema = schema

    async def get_data(
            self,
            data_id: int = None,
            v_start_sql: SelectType = None,
            v_select_from: list[Any] = None,
            v_join: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_outerjoin: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_options: list[_AbstractLoad] = None,
            v_where: list[BinaryExpression] = None,
            v_order: str = None,
            v_order_field: str = None,
            v_return_none: bool = False,
            v_schema: Any = None,
            **kwargs
    ) -> Any:
        """
        获取单个数据，默认使用 ID 查询，否则使用关键词查询

        :param data_id: 数据 ID
        :param v_start_sql: 初始 sql
        :param v_select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param v_join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param v_outerjoin: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param v_options: 用于为查询添加附加选项，如预加载、延迟加载等。
        :param v_where: 当前表查询条件，原始表达式
        :param v_order: 排序，默认正序，为 desc 是倒叙
        :param v_order_field: 排序字段
        :param v_return_none: 是否返回空 None，否认 抛出异常，默认抛出异常
        :param v_schema: 指定使用的序列化对象
        :param kwargs: 查询参数
        :return: 默认返回 ORM 对象，如果存在 v_schema 则会返回 v_schema 结果
        """
        if not isinstance(v_start_sql, SelectType):
            v_start_sql = select(self.model).where(self.model.is_delete == False)

        if data_id:
            v_start_sql = v_start_sql.where(self.model.id == data_id)

        queryset: ScalarResult = await self.filter_core(
            v_start_sql=v_start_sql,
            v_select_from=v_select_from,
            v_join=v_join,
            v_outerjoin=v_outerjoin,
            v_options=v_options,
            v_where=v_where,
            v_order=v_order,
            v_order_field=v_order_field,
            v_return_sql=False,
            **kwargs
        )

        if v_options:
            data = queryset.unique().first()
        else:
            data = queryset.first()

        if not data and v_return_none:
            return None

        if data and v_schema:
            return v_schema.model_validate(data).model_dump()

        if data:
            return data

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到此数据")

    async def get_datas(
            self,
            page: int = 1,
            limit: int = 10,
            v_start_sql: SelectType = None,
            v_select_from: list[Any] = None,
            v_join: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_outerjoin: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_options: list[_AbstractLoad] = None,
            v_where: list[BinaryExpression] = None,
            v_order: str = None,
            v_order_field: str = None,
            v_return_count: bool = False,
            v_return_scalars: bool = False,
            v_return_objs: bool = False,
            v_schema: Any = None,
            **kwargs
    ) -> list[Any] | ScalarResult | tuple:
        """
        获取数据列表

        :param page: 页码
        :param limit: 当前页数据量
        :param v_start_sql: 初始 sql
        :param v_select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param v_join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param v_outerjoin: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param v_options: 用于为查询添加附加选项，如预加载、延迟加载等。
        :param v_where: 当前表查询条件，原始表达式
        :param v_order: 排序，默认正序，为 desc 是倒叙
        :param v_order_field: 排序字段
        :param v_return_count: 默认为 False，是否返回 count 过滤后的数据总数，不会影响其他返回结果，会一起返回为一个数组
        :param v_return_scalars: 返回scalars后的结果
        :param v_return_objs: 是否返回对象
        :param v_schema: 指定使用的序列化对象
        :param kwargs: 查询参数，使用的是自定义表达式
        :return: 返回值优先级：v_return_scalars > v_return_objs > v_schema
        """
        sql: SelectType = await self.filter_core(
            v_start_sql=v_start_sql,
            v_select_from=v_select_from,
            v_join=v_join,
            v_outerjoin=v_outerjoin,
            v_options=v_options,
            v_where=v_where,
            v_order=v_order,
            v_order_field=v_order_field,
            v_return_sql=True,
            **kwargs
        )

        count = 0
        if v_return_count:
            count_sql = select(func.count()).select_from(sql.alias())
            count_queryset = await self.db.execute(count_sql)
            count = count_queryset.one()[0]

        if limit != 0:
            sql = sql.offset((page - 1) * limit).limit(limit)

        queryset = await self.db.scalars(sql)

        if v_return_scalars:
            if v_return_count:
                return queryset, count
            return queryset

        if v_options:
            result = queryset.unique().all()
        else:
            result = queryset.all()

        if v_return_objs:
            if v_return_count:
                return list(result), count
            return list(result)

        datas = [await self.out_dict(i, v_schema=v_schema) for i in result]
        if v_return_count:
            return datas, count
        return datas

    async def get_count(
            self,
            v_select_from: list[Any] = None,
            v_join: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_outerjoin: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_where: list[BinaryExpression] = None,
            **kwargs
    ) -> int:
        """
        获取数据总数

        :param v_select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param v_join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param v_outerjoin: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param v_where: 当前表查询条件，原始表达式
        :param kwargs: 查询参数
        """
        v_start_sql = select(func.count(self.model.id))
        sql = await self.filter_core(
            v_start_sql=v_start_sql,
            v_select_from=v_select_from,
            v_join=v_join,
            v_outerjoin=v_outerjoin,
            v_where=v_where,
            v_return_sql=True,
            **kwargs
        )
        queryset = await self.db.execute(sql)
        return queryset.one()[0]

    async def create_data(
            self,
            data,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建单个数据

        :param data: 创建数据
        :param v_options: 指示应使用select在预加载中加载给定的属性。
        :param v_schema: ，指定使用的序列化对象
        :param v_return_obj: ，是否返回对象
        """
        if isinstance(data, dict):
            obj = self.model(**data)
        else:
            obj = self.model(**data.model_dump())
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    # async def create_datas(self, datas: list[dict]) -> None:
    #     """
    #     批量创建数据，暂不启用
    #     SQLAlchemy 2.0 批量插入不支持 MySQL 返回对象：
    #     https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#getting-new-objects-with-returning
    #
    #     :param datas: 字典数据列表
    #     """
    #     await self.db.execute(insert(self.model), datas)
    #     await self.db.flush()

    async def put_data(
            self,
            data_id: int,
            data: Any,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新单个数据
        :param data_id: 修改行数据的 ID
        :param data: 数据内容
        :param v_options: 指示应使用select在预加载中加载给定的属性。
        :param v_return_obj: ，是否返回对象
        :param v_schema: ，指定使用的序列化对象
        """
        obj = await self.get_data(data_id, v_options=v_options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
        """
        删除多条数据
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        if v_soft:
            await self.db.execute(
                update(self.model).where(self.model.id.in_(ids)).values(
                    delete_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    is_delete=True,
                    **kwargs
                )
            )
        else:
            await self.db.execute(delete(self.model).where(self.model.id.in_(ids)))
        await self.flush()

    async def flush(self, obj: Any = None) -> Any:
        """
        刷新到数据库
        """
        if obj:
            self.db.add(obj)
        await self.db.flush()
        if obj:
            await self.db.refresh(obj)
        return obj

    async def out_dict(
            self,
            obj: Any,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        序列化
        :param obj:
        :param v_options: 指示应使用select在预加载中加载给定的属性。
        :param v_return_obj: ，是否返回对象
        :param v_schema: ，指定使用的序列化对象
        :return:
        """
        if v_options:
            obj = await self.get_data(obj.id, v_options=v_options)
        if v_return_obj:
            return obj
        if v_schema:
            return v_schema.model_validate(obj).model_dump()
        return self.schema.model_validate(obj).model_dump()

    async def filter_core(
            self,
            v_start_sql: SelectType = None,
            v_select_from: list[Any] = None,
            v_join: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_outerjoin: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_options: list[_AbstractLoad] = None,
            v_where: list[BinaryExpression] = None,
            v_order: str = None,
            v_order_field: str = None,
            v_return_sql: bool = False,
            **kwargs
    ) -> ScalarResult | SelectType:
        """
        数据过滤核心功能

        :param v_start_sql: 初始 sql
        :param v_select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param v_join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param v_outerjoin: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param v_options: 用于为查询添加附加选项，如预加载、延迟加载等。
        :param v_where: 当前表查询条件，原始表达式
        :param v_order: 排序，默认正序，为 desc 是倒叙
        :param v_order_field: 排序字段
        :param v_return_sql: 是否直接返回 sql
        :return: 返回过滤后的总数居 或 sql
        """
        if not isinstance(v_start_sql, SelectType):
            v_start_sql = select(self.model).where(self.model.is_delete == False)

        sql = self.add_relation(
            v_start_sql=v_start_sql,
            v_select_from=v_select_from,
            v_join=v_join,
            v_outerjoin=v_outerjoin,
            v_options=v_options
        )

        if v_where:
            sql = sql.where(*v_where)

        sql = self.add_filter_condition(sql, **kwargs)

        if v_order_field and (v_order in self.ORDER_FIELD):
            sql = sql.order_by(getattr(self.model, v_order_field).desc(), self.model.id.desc())
        elif v_order_field:
            sql = sql.order_by(getattr(self.model, v_order_field), self.model.id)
        elif v_order in self.ORDER_FIELD:
            sql = sql.order_by(self.model.id.desc())

        if v_return_sql:
            return sql

        queryset = await self.db.scalars(sql)

        return queryset

    def add_relation(
            self,
            v_start_sql: SelectType,
            v_select_from: list[Any] = None,
            v_join: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_outerjoin: list[list[str | InstrumentedAttribute, BinaryExpression | None]] = None,
            v_options: list[_AbstractLoad] = None,
    ) -> SelectType:
        """
        :param v_start_sql: 初始 sql
        :param v_select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param v_join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param v_outerjoin: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param v_options: 用于为查询添加附加选项，如预加载、延迟加载等。
        """
        if v_select_from:
            v_start_sql = v_start_sql.select_from(*v_select_from)

        if v_join:
            for relation in v_join:
                table = relation[0]
                if isinstance(table, str):
                    table = getattr(self.model, table)
                if len(relation) == 2:
                    v_start_sql = v_start_sql.join(table, relation[1])
                else:
                    v_start_sql = v_start_sql.join(table)

        if v_outerjoin:
            for relation in v_outerjoin:
                table = relation[0]
                if isinstance(table, str):
                    table = getattr(self.model, table)
                if len(relation) == 2:
                    v_start_sql = v_start_sql.outerjoin(table, relation[1])
                else:
                    v_start_sql = v_start_sql.outerjoin(table)

        if v_options:
            v_start_sql = v_start_sql.options(*v_options)

        return v_start_sql

    def add_filter_condition(self, sql: SelectType, **kwargs) -> SelectType:
        """
        添加过滤条件
        :param sql:
        :param kwargs: 关键词参数
        """
        conditions = self.__dict_filter(**kwargs)
        if conditions:
            sql = sql.where(*conditions)
        return sql

    def __dict_filter(self, **kwargs) -> list[BinaryExpression]:
        """
        字典过滤
        :param model:
        :param kwargs:
        """
        conditions = []
        for field, value in kwargs.items():
            if value is not None and value != "":
                attr = getattr(self.model, field)
                if isinstance(value, tuple):
                    if len(value) == 1:
                        if value[0] == "None":
                            conditions.append(attr.is_(None))
                        elif value[0] == "not None":
                            conditions.append(attr.isnot(None))
                        else:
                            raise CustomException("SQL查询语法错误")
                    elif len(value) == 2 and value[1] not in [None, [], ""]:
                        if value[0] == "date":
                            # 根据日期查询， 关键函数是：func.time_format和func.date_format
                            conditions.append(func.date_format(attr, "%Y-%m-%d") == value[1])
                        elif value[0] == "like":
                            conditions.append(attr.like(f"%{value[1]}%"))
                        elif value[0] == "in":
                            conditions.append(attr.in_(value[1]))
                        elif value[0] == "between" and len(value[1]) == 2:
                            conditions.append(attr.between(value[1][0], value[1][1]))
                        elif value[0] == "month":
                            conditions.append(func.date_format(attr, "%Y-%m") == value[1])
                        elif value[0] == "!=":
                            conditions.append(attr != value[1])
                        elif value[0] == ">":
                            conditions.append(attr > value[1])
                        elif value[0] == "<=":
                            conditions.append(attr <= value[1])
                        else:
                            raise CustomException("SQL查询语法错误")
                else:
                    conditions.append(attr == value)
        return conditions
