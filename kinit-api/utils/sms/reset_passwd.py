#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/14 16:58 
# @File           : reset_passwd.py
# @IDE            : PyCharm
# @desc           : 重置密码

from typing import List
from redis.asyncio import Redis
from .aliyun import AliyunSMS


class ResetPasswordSMS(AliyunSMS):

    def __init__(self, telephones: List[str], rd: Redis = None):
        super().__init__(telephones, rd)

        self.sign_conf = "sms_sign_name_2"
        self.template_code_conf = "sms_template_code_2"

    async def main_async(self, password: str) -> List[bool]:
        """
        主程序入口，异步方式

        redis 对象必填
        :param password: 新密码
        """
        return await super().main_async(password=password)

    def main(self, password: str) -> List[bool]:
        """
        主程序入口，同步方式

        :param password: 新密码
        """
        return super().main(password=password)

    def _get_template_param(self, **kwargs) -> str:
        """
        获取模板参数

        可以被子类继承的受保护的私有方法
        """
        password = kwargs.get("password")
        template_param = '{"password":"%s"}' % password
        return template_param
