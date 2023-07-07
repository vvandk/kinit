import atexit
import datetime
import json
import random
from enum import Enum
from apscheduler.jobstores.base import ConflictingIdError
from core.scheduler import Scheduler
from core.mongo import get_database as get_mongo
from application.settings import MONGO_DB_NAME, MONGO_DB_URL, REDIS_DB_URL, SUBSCRIBE, SCHEDULER_TASK, \
    SCHEDULER_TASK_RECORD
from core.redis import get_database as get_redis
from core.logger import logger


class ScheduledTask:

    class JobExecStrategy(Enum):
        interval = "interval"
        date = "date"
        cron = "cron"
        once = "once"

    def __init__(self):
        self.mongo = None
        self.scheduler = None
        self.rd = None

    def add_job(self, exec_strategy: str, job_params: dict) -> None:
        """
        添加定时任务

        :param exec_strategy: 执行策略
        :param job_params: 执行参数
        :return:
        """
        name = job_params.get("name", None)
        error_info = None
        try:
            if exec_strategy == self.JobExecStrategy.interval.value:
                self.scheduler.add_interval_job(**job_params)
            elif exec_strategy == self.JobExecStrategy.cron.value:
                self.scheduler.add_cron_job(**job_params)
            elif exec_strategy == self.JobExecStrategy.date.value:
                self.scheduler.add_date_job(**job_params)
            elif exec_strategy == self.JobExecStrategy.once.value:
                # 这种方式会自动执行事件监听器，用于保存执行任务完成后的日志
                job_params["name"] = f"{name}-temp-{random.randint(1000, 9999)}"
                self.scheduler.add_date_job(**job_params, expression=datetime.datetime.now())
            else:
                raise ValueError("无效的触发器")
        except ConflictingIdError as e:
            # 任务编号已存在，重复添加报错
            error_info = "任务编号已存在"
        except ValueError as e:
            error_info = e.__str__()

        if error_info:
            logger.error(f"任务编号：{name}，报错：{error_info}")
            self.error_record(name, error_info)

    def error_record(self, name: str, error_info: str) -> None:
        """
        添加任务失败记录，并且将任务状态改为 False

        :param name: 任务编号
        :param error_info: 报错信息
        :return:
        """
        try:
            self.mongo.put_data(SCHEDULER_TASK, name, {"is_active": False})
            task = self.mongo.get_data(SCHEDULER_TASK, name)
            # 执行你想要在任务执行前执行的代码
            result = {
                "job_id": name,
                "job_class": task.get("job_class", None),
                "name": task.get("name", None),
                "group": task.get("group", None),
                "exec_strategy": task.get("exec_strategy", None),
                "expression": task.get("expression", None),
                "start_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "process_time": 0,
                "retval": "任务添加失败",
                "exception": error_info,
                "traceback": None
            }
            self.mongo.create_data(SCHEDULER_TASK_RECORD, result)
        except ValueError as e:
            logger.error(f"任务编号：{name}, 报错：{e}")

    def run(self) -> None:
        """
        启动监听订阅消息（阻塞）

        :return:
        """
        self.start_mongo()
        self.start_scheduler()
        self.start_redis()

        pubsub = self.rd.subscribe(SUBSCRIBE)

        logger.info("已成功启动程序，等待接收消息...")
        print("已成功启动程序，等待接收消息...")

        # 处理接收到的消息
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'].decode('utf-8'))
                operation = data.get("operation")
                task = data.get("task")
                content = f"接收到任务：任务操作方式({operation})，任务详情：{task}"
                logger.info(content)
                print(content)
                getattr(self, operation)(**task)
            else:
                print("意外", message)

    def start_mongo(self) -> None:
        """
        启动 mongo

        :return:
        """
        self.mongo = get_mongo()
        self.mongo.connect_to_database(MONGO_DB_URL, MONGO_DB_NAME)
        print("成功连接 MongoDB")

    def start_scheduler(self) -> None:
        """
        启动定时任务

        :return:
        """
        self.scheduler = Scheduler()
        self.scheduler.start()
        print("成功启动 Scheduler")

    def start_redis(self) -> None:
        """
        启动 redis

        :return:
        """
        self.rd = get_redis()
        self.rd.connect_to_database(REDIS_DB_URL)
        print("成功连接 Redis")

    def close(self) -> None:
        """
        # pycharm 执行停止，该函数无法正常被执行，怀疑是因为阻塞导致或 pycharm 的强制退出导致
        # 报错导致得退出，会被执行
        关闭程序

        :return:
        """
        self.mongo.close_database_connection()
        self.scheduler.shutdown()
        self.rd.close_database_connection()


if __name__ == '__main__':
    main = ScheduledTask()
    atexit.register(main.close)
    main.run()

