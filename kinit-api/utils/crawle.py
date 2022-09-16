#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/2/24 17:02
# @File           : crawle.py
# @IDE            : PyCharm
# @desc           : 爬虫

import requests
from core.logger import logger


def get_schedule_data():
    """
    获取足球赛程表
    """
    logger.info("开始获取足球赛程")
    url = "https://webapi.sporttery.cn/gateway/jc/football/getMatchCalculatorV1.qry?poolCode=hhad,had&channel=c"
    res = requests.get(url)
    if res.status_code != 200:
        logger.error("获取足球赛程失败！")
        return False
    data = res.json()
    if data.get("errorCode") != "0":
        logger.error("获取足球赛程失败！")
        return False
    return data.get("value").get("matchInfoList")
