import redis


class RedisManage:
    """
    redis 数据库管理器
    """

    rd: redis.Redis = None

    def connect_to_database(self, path: str) -> None:
        """
        连接 redis 数据库

        :param path: mongodb 链接地址
        :return:
        """
        self.rd = redis.from_url(path)

    def close_database_connection(self) -> None:
        """
        关闭 redis 连接

        :return:
        """
        self.rd.close()

    def subscribe(self, channel: str):
        """
        订阅

        :param channel: 频道
        :return:
        """
        pubsub = self.rd.pubsub()
        pubsub.subscribe(channel)
        return pubsub
