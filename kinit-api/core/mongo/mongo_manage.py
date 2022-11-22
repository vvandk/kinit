import json
from bson.json_util import dumps
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.mongo import DatabaseManage
from pymongo.results import InsertOneResult
from pydantic import BaseModel


class MongoManage(DatabaseManage):
    """
    This class extends from ./database_manage.py
    which have the abstract methods to be re-used here.
    博客：https://www.cnblogs.com/aduner/p/13532504.html
    mongodb 官网：https://www.mongodb.com/docs/drivers/motor/
    motor 文档：https://motor.readthedocs.io/en/stable/
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str, db_name: str):
        print("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client[db_name]

    async def close_database_connection(self):
        self.client.close()
        print("MongoDB connection closed")

    async def create_data(self, collection: str, data: dict) -> InsertOneResult:
        return await self.db[collection].insert_one(data)

    async def get_datas(self, collection: str, schema: BaseModel = None, **kwargs):
        """
        使用 find() 要查询的一组文档。 find() 没有I / O，也不需要 await 表达式。它只是创建一个 AsyncIOMotorCursor 实例
        当您调用 to_list() 或为循环执行异步时 (async for) ，查询实际上是在服务器上执行的。
        """
        page = kwargs.pop("page", 1)
        limit = kwargs.pop("limit", 10)
        order = kwargs.pop("v_order", None)
        order_field = kwargs.pop("v_order_field", None)

        params = self.filter_condition(**kwargs)
        cursor = self.db[collection].find(params)

        # 对查询应用排序(sort)，跳过(skip)或限制(limit)
        cursor.sort("create_datetime", -1).skip((page - 1) * limit).limit(limit)

        datas = []
        async for row in cursor:
            del row['_id']
            data = json.loads(dumps(row))
            if schema:
                data = schema.parse_obj(data).dict()
            datas.append(data)
        return datas

    async def get_count(self, collection: str, **kwargs) -> int:
        params = self.filter_condition(**kwargs)
        return await self.db[collection].count_documents(params)

    @classmethod
    def filter_condition(cls, **kwargs):
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
            else:
                params[k] = v
        return params
