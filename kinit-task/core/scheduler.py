#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/21 10:10 
# @File           : scheduler.py
# @IDE            : PyCharm
# @desc           : 简要说明

import datetime
import importlib
from typing import List
import re
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.job import Job
from .listener import before_job_execution
from apscheduler.events import EVENT_JOB_EXECUTED
from application.settings import MONGO_DB_NAME, SCHEDULER_TASK_JOBS, TASKS_ROOT
from core.mongo import get_database


class Scheduler:
    TASK_DIR = TASKS_ROOT
    COLLECTION = SCHEDULER_TASK_JOBS

    def __init__(self):
        self.scheduler = None
        self.db = None

    def start(self, listener: bool = True) -> None:
        """
        创建调度器

        :return:
        """
        self.scheduler = BackgroundScheduler()
        if listener:
            # 注册事件监听器
            self.scheduler.add_listener(before_job_execution, EVENT_JOB_EXECUTED)
        self.scheduler.add_jobstore(self.__get_mongodb_job_store())
        self.scheduler.start()

    def __get_mongodb_job_store(self) -> MongoDBJobStore:
        """
        获取 MongoDBJobStore

        :return: MongoDBJobStore
        """
        self.db = get_database()
        return MongoDBJobStore(database=MONGO_DB_NAME, collection=self.COLLECTION, client=self.db.client)

    def add_job(
            self,
            job_class: str,
            trigger: CronTrigger | DateTrigger | IntervalTrigger,
            name: str = None,
            *args,
            **kwargs
    ) -> None | Job:
        """
        date触发器用于在指定的日期和时间触发一次任务。它适用于需要在特定时间点执行一次的任务，例如执行一次备份操作。

        :param job_class: 类路径
        :param trigger: 触发条件
        :param name: 任务名称
        :return:
        """
        job_class = self.__import_module(job_class)
        if job_class:
            return self.scheduler.add_job(job_class.main, trigger=trigger, args=args, kwargs=kwargs, id=name)
        else:
            raise ValueError(f"添加任务失败，未找到该模块下的方法：{job_class}")

    def add_cron_job(
            self,
            job_class: str,
            expression: str,
            start_date: str = None,
            end_date: str = None,
            timezone: str = "Asia/Shanghai",
            name: str = None,
            args: tuple = (),
            **kwargs
    ) -> None | Job:
        """
        通过 cron 表达式添加定时任务

        :param job_class: 类路径
        :param expression: cron 表达式，六位或七位，分别表示秒、分钟、小时、天、月、星期几、年
        :param start_date: 触发器的开始日期时间。可选参数，默认为 None。
        :param end_date: 触发器的结束日期时间。可选参数，默认为 None。
        :param timezone: 时区，表示触发器应用的时区。可选参数，默认为 None，使用上海默认时区。
        :param name: 任务名称
        :param args: 非关键字参数
        :return:
        """
        second, minute, hour, day, month, day_of_week, year = self.__parse_cron_expression(expression)
        trigger = CronTrigger(
            second=second,
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
            year=year,
            start_date=start_date,
            end_date=end_date,
            timezone=timezone
        )
        return self.add_job(job_class, trigger, name, *args, **kwargs)

    def add_date_job(self, job_class: str, expression: str, name: str = None, args: tuple = (), **kwargs) -> None | Job:
        """
        date触发器用于在指定的日期和时间触发一次任务。它适用于需要在特定时间点执行一次的任务，例如执行一次备份操作。

        :param job_class: 类路径
        :param expression: date
        :param name: 任务名称
        :param args: 非关键字参数
        :return:
        """
        trigger = DateTrigger(run_date=expression)
        return self.add_job(job_class, trigger, name, *args, **kwargs)

    def add_interval_job(
            self,
            job_class: str,
            expression: str,
            start_date: str | datetime.datetime = None,
            end_date: str | datetime.datetime = None,
            timezone: str = "Asia/Shanghai",
            jitter: int = None,
            name: str = None,
            args: tuple = (),
            **kwargs
    ) -> None | Job:
        """
        date触发器用于在指定的日期和时间触发一次任务。它适用于需要在特定时间点执行一次的任务，例如执行一次备份操作。

        :param job_class: 类路径
        :param expression：interval 表达式，分别为：秒、分、时、天、周，例如，设置 10 * * * * 表示每隔 10 秒执行一次任务。
        :param end_date: 表示任务的结束时间，可以设置为 datetime 对象或者字符串。
                         例如，设置 end_date='2023-06-23 10:00:00' 表示任务在 2023 年 6 月 23 日 10 点结束。
        :param start_date: 表示任务的起始时间，可以设置为 datetime 对象或者字符串。
                           例如，设置 start_date='2023-06-22 10:00:00' 表示从 2023 年 6 月 22 日 10 点开始执行任务。
        :param timezone：表示时区，可以设置为字符串或 pytz.timezone 对象。例如，设置 timezone='Asia/Shanghai' 表示使用上海时区。
        :param jitter：表示时间抖动，可以设置为整数或浮点数。例如，设置 jitter=2 表示任务的执行时间会在原定时间上随机增加 0~2 秒的时间抖动。
        :param name: 任务名称
        :param args: 非关键字参数
        :return:
        """
        second, minute, hour, day, week = self.__parse_interval_expression(expression)
        trigger = IntervalTrigger(
            weeks=week,
            days=day,
            hours=hour,
            minutes=minute,
            seconds=second,
            start_date=start_date,
            end_date=end_date,
            timezone=timezone,
            jitter=jitter
        )
        return self.add_job(job_class, trigger, name, *args, **kwargs)

    def run_job(self, job_class: str, args: tuple = (), **kwargs) -> None:
        """
        立即执行一次任务，但不会执行监听器，只适合只需要执行任务，不需要记录的任务

        :param job_class: 类路径
        :param args: 类路径
        :return: 类实例
        """
        job_class = self.__import_module(job_class)
        job_class.main(*args, **kwargs)

    def remove_job(self, name: str) -> None:
        """
        删除任务

        :param name: 任务名称
        :return:
        """
        try:
            self.scheduler.remove_job(name)
        except JobLookupError as e:
            raise ValueError(f"删除任务失败, 报错：{e}")

    def get_job(self, name: str) -> Job:
        """
        获取任务

        :param name: 任务名称
        :return:
        """
        return self.scheduler.get_job(name)

    def has_job(self, name: str) -> bool:
        """
        判断任务是否存在

        :param name: 任务名称
        :return:
        """
        if self.get_job(name):
            return True
        else:
            return False

    def get_jobs(self) -> List[Job]:
        """
        获取所有任务

        :return:
        """
        return self.scheduler.get_jobs()

    def get_job_names(self) -> List[str]:
        """
        获取所有任务

        :return:
        """
        jobs = self.scheduler.get_jobs()
        return [job.id for job in jobs]

    def __import_module(self, expression: str):
        """
        反射模块

        :param expression: 类路径
        :return: 类实例
        """
        module, args = self.__parse_string_to_class(expression)
        module_pag = self.TASK_DIR + '.' + module[0:module.rindex(".")]
        module_class = module[module.rindex(".") + 1:]
        try:
            # 动态导入模块
            pag = importlib.import_module(module_pag)
            return getattr(pag, module_class)(*args)
        except ModuleNotFoundError:
            raise ValueError(f"未找到该模块：{module_pag}")
        except AttributeError:
            raise ValueError(f"未找到该模块下的方法：{module_class}")
        except TypeError as e:
            raise ValueError(f"参数传递错误：{args}, 详情：{e}")

    @staticmethod
    def __parse_cron_expression(expression: str) -> tuple:
        """
        解析 cron 表达式

        :param expression: cron 表达式，支持六位或七位，分别表示秒、分钟、小时、天、月、星期几、年
        :return: 解析后的秒、分钟、小时、天、月、星期几、年字段的元组
        """
        fields = expression.strip().split()

        if len(fields) not in (6, 7):
            raise ValueError("无效的 Cron 表达式")

        parsed_fields = [None if field in ('*', '?') else field for field in fields]
        if len(fields) == 6:
            parsed_fields.append(None)

        return tuple(parsed_fields)

    @staticmethod
    def __parse_interval_expression(expression: str) -> tuple:
        """
        解析 interval 表达式

        :param expression: interval 表达式，分别为：秒、分、时、天、周，例如，设置 10 * * * * 表示每隔 10 秒执行一次任务。
        :return:
        """
        # 将传入的 interval 表达式拆分为不同的字段
        fields = expression.strip().split()

        if len(fields) != 5:
            raise ValueError("无效的 interval 表达式")

        parsed_fields = [int(field) if field != '*' else 0 for field in fields]
        return tuple(parsed_fields)

    @classmethod
    def __parse_string_to_class(cls, expression: str) -> tuple:
        """
        使用正则表达式匹配类路径和参数

        :param expression: 表达式
        :return:
        """
        pattern = r'([\w.]+)(?:\((.*)\))?'
        match = re.match(pattern, expression)

        if match:
            class_path = match.group(1)
            arguments = match.group(2)

            if arguments:
                arguments = cls.__parse_arguments(arguments)
            else:
                arguments = []

            return class_path, arguments

        return None, None

    @staticmethod
    def __parse_arguments(args_str) -> list:
        """
        解析类路径参数字符串

        :param args_str: 类参数字符串
        :return:
        """
        arguments = []

        for arg in re.findall(r'"([^"]*)"|(\d+\.\d+)|(\d+)|([Tt]rue|[Ff]alse)', args_str):
            if arg[0]:
                # 字符串参数
                arguments.append(arg[0])
            elif arg[1]:
                # 浮点数参数
                arguments.append(float(arg[1]))
            elif arg[2]:
                # 整数参数
                arguments.append(int(arg[2]))
            elif arg[3]:
                # 布尔参数
                if arg[3].lower() == 'true':
                    arguments.append(True)
                else:
                    arguments.append(False)

        return arguments

    def shutdown(self) -> None:
        """
        关闭调度器

        :return:
        """
        self.scheduler.shutdown()
