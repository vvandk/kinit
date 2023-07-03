#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/21 10:08 
# @File           : mian.py
# @IDE            : PyCharm
# @desc           : 简要说明
import datetime
import time


class Test:

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def main(self) -> str:
        """
        主入口函数

        :return:
        """
        print('{}, 定时任务测试实例，参数为: {}, {}'.format(datetime.datetime.now(), self.name, self.age))
        time.sleep(3)
        return '任务执行完成'
