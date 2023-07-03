#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/21 14:42 
# @File           : listener.py
# @IDE            : PyCharm
# @desc           : 简要说明

import datetime
import json
from apscheduler.events import JobExecutionEvent
from core.mongo import get_database
import pytz
from application.settings import SCHEDULER_TASK_RECORD, SCHEDULER_TASK
from core.logger import logger


def before_job_execution(event: JobExecutionEvent):
    # print("在执行定时任务前执行的代码...")
    shanghai_tz = pytz.timezone("Asia/Shanghai")
    start_time: datetime.datetime = event.scheduled_run_time.astimezone(shanghai_tz)
    end_time = datetime.datetime.now(shanghai_tz)
    process_time = (end_time - start_time).total_seconds()
    job_id = event.job_id
    if "-temp-" in job_id:
        job_id = job_id.split("-")[0]
    # print("任务标识符：", event.job_id)
    # print("任务开始执行时间：", start_time.strftime("%Y-%m-%d %H:%M:%S"))
    # print("任务执行完成时间：", end_time.strftime("%Y-%m-%d %H:%M:%S"))
    # print("任务耗时（秒）：", process_time)
    # print("任务返回值：", event.retval)
    # print("异常信息：", event.exception)
    # print("堆栈跟踪：", event.traceback)

    result = {
        "job_id": job_id,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "process_time": process_time,
        "retval": json.dumps(event.retval),
        "exception": json.dumps(event.exception),
        "traceback": json.dumps(event.traceback)
    }

    db = get_database()
    try:
        task = db.get_data(SCHEDULER_TASK, job_id, is_object_id=True)
        result["job_class"] = task.get("job_class", None)
        result["name"] = task.get("name", None)
        result["group"] = task.get("group", None)
        result["exec_strategy"] = task.get("exec_strategy", None)
        result["expression"] = task.get("expression", None)
    except ValueError as e:
        result["exception"] = str(e)
        logger.error(f"任务编号：{event.job_id}，报错：{e}")
    db.create_data(SCHEDULER_TASK_RECORD, result)

