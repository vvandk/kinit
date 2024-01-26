import redis


class RedisManage:
    """
    redis 数据库管理器
    """

    rd: redis.Redis = None

    def connect_to_database(self, path: str) -> None:
        """
        连接 redis 数据库
        :param path: redis 连接地址
        :return:
        """
        self.rd = redis.from_url(path)
        self.test_connect()

    def test_connect(self) -> None:
        """
        测试连接
        :return:
        """
        try:
            # 发送PING命令
            response = self.rd.ping()
            if response:
                print("Redis 连接成功")
            else:
                print("Redis 连接失败")
        except redis.exceptions.RedisError as e:
            # 捕获并处理任何Redis错误
            raise redis.exceptions.RedisError(f"Redis 连接失败: {e}")

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
