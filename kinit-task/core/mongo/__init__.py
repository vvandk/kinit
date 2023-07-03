from .mongo_manage import MongoManage

db = MongoManage()


def get_database() -> MongoManage:
    return db
