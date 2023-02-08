from abc import abstractmethod
from typing import Any


class DatabaseManage:
    """
    This class is meant to be extended from
    ./mongo_manage.py which will be the actual connection to mongodb.
    """

    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    # database connect and close connections
    @abstractmethod
    async def connect_to_database(self, path: str, db_name: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def create_data(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def get_datas(
            self,
            collection: str,
            page: int = 1,
            limit: int = 10,
            v_schema: Any = None,
            v_order: str = None,
            v_order_field: str = None,
            **kwargs
    ):
        pass

    @abstractmethod
    async def get_count(self, collection: str, **kwargs) -> int:
        pass
