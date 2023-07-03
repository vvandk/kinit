from .redis_manage import RedisManage

db = RedisManage()


def get_database() -> RedisManage:
    return db
