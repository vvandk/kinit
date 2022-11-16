from .database_manage import DatabaseManage
from .mongo_manage import MongoManage
from application.settings import MONGO_DB_ENABLE
from core.exception import CustomException
from utils import status

db = MongoManage()


async def get_database() -> DatabaseManage:
    if not MONGO_DB_ENABLE:
        raise CustomException(msg="请先开启 MongoDB 数据库连接！", code=status.HTTP_ERROR)
    return db
