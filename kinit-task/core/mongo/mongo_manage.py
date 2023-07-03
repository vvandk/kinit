import datetime
from typing import Any
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.mongo_client import MongoClient as MongoClientType
from pymongo.database import Database


class MongoManage:
    """
    mongodb 数据库管理器
    mongodb 官网：https://www.mongodb.com/docs/drivers/pymongo/
    """

    client: MongoClientType = None
    db: Database = None

    def connect_to_database(self, path: str, db_name: str) -> None:
        """
        连接 mongodb 数据库

        :param path: mongodb 链接地址
        :param db_name: 数据库名称
        :return:
        """
        self.client = MongoClient(path)
        self.db = self.client[db_name]

    def close_database_connection(self) -> None:
        """
        关闭 mongodb 数据库连接

        :return:
        """
        self.client.close()

    def create_data(self, collection: str, data: dict) -> InsertOneResult:
        """
        创建单个数据

        :param collection: 集合
        :param data: 数据
        """
        data['create_datetime'] = datetime.datetime.now()
        data['update_datetime'] = datetime.datetime.now()
        result = self.db[collection].insert_one(data)
        # 判断插入是否成功
        if result.acknowledged:
            return result
        else:
            raise ValueError("创建新数据失败")

    def get_data(
            self,
            collection: str,
            _id: str = None,
            v_return_none: bool = False,
            v_schema: Any = None,
            is_object_id: bool = False,
            **kwargs
    ) -> dict | None:
        """
        获取单个数据，默认使用 ID 查询，否则使用关键词查询

        :param collection: 集合
        :param _id: 数据 ID
        :param v_return_none: 是否返回空 None，否则抛出异常，默认抛出异常
        :param is_object_id: 是否为 ObjectId
        :param v_schema: 指定使用的序列化对象
        """
        if _id and is_object_id:
            kwargs["_id"] = ObjectId(_id)
        params = self.filter_condition(**kwargs)
        data = self.db[collection].find_one(params)
        if not data and v_return_none:
            return None
        elif not data:
            raise ValueError("查询单个数据失败，未找到匹配的数据")
        elif data and v_schema:
            return v_schema(**data).dict()
        return data

    def put_data(self, collection: str, _id: str, data: dict, is_object_id: bool = False) -> UpdateResult:
        """
        更新数据
        """
        new_data = {'$set': data}
        result = self.db[collection].update_one({'_id': ObjectId(_id) if is_object_id else _id}, new_data)

        if result.matched_count > 0:
            return result
        else:
            raise ValueError("更新数据失败，未找到匹配的数据")

    @classmethod
    def filter_condition(cls, **kwargs) -> dict:
        """
        过滤条件
        """
        params = {}
        for k, v in kwargs.items():
            if not v:
                continue
            elif isinstance(v, tuple):
                if v[0] == "like" and v[1]:
                    params[k] = {'$regex': v[1]}
                elif v[0] == "between" and len(v[1]) == 2:
                    params[k] = {'$gte': f"{v[1][0]} 00:00:00", '$lt': f"{v[1][1]} 23:59:59"}
                elif v[0] == "ObjectId" and v[1]:
                    try:
                        params[k] = ObjectId(v[1])
                    except InvalidId:
                        raise ValueError("任务编号格式不正确！")
            else:
                params[k] = v
        return params
