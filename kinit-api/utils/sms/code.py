#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/14 15:55 
# @File           : code.py
# @IDE            : PyCharm
# @desc           : 发送验证码短信

import datetime
import warnings
from redis.asyncio import Redis
from .aliyun import AliyunSMS
from core.logger import logger
from core.exception import CustomException


class CodeSMS(AliyunSMS):

    def __init__(self, telephone: str, rd: Redis):
        super().__init__([telephone], rd)

        self.telephone = telephone
        self.sign_conf = "sms_sign_name_1"
        self.template_code_conf = "sms_template_code_1"

    async def main_async(self) -> bool:
        """
        主程序入口，异步方式

        redis 对象必填
        """

        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if await self.rd.get(self.telephone + "_flag_"):
            logger.error(f'{send_time} {self.telephone} 短信发送失败，短信发送过于频繁')
            raise CustomException(msg="短信发送频繁", code=400)
        await self._get_settings_async()
        result = await self._send_async(self.telephone)
        if result:
            await self.rd.set(self.telephone, self.code, self.valid_time)
            await self.rd.set(self.telephone + "_flag_", self.code, self.send_interval)
        return result

    async def main(self) -> None:
        """
        主程序入口，同步方式
        """
        warnings.warn("此方法已废弃，如需要请重写该方法", DeprecationWarning)

    async def check_sms_code(self, code: str) -> bool:
        """
        检查短信验证码是否正确
        """
        if code and code == await self.rd.get(self.telephone):
            await self.rd.delete(self.telephone)
            await self.rd.delete(self.telephone + "_flag_")
            return True
        return False

    def _get_template_param(self, **kwargs) -> str:
        """
        获取模板参数

        可以被子类继承的受保护的私有方法
        """
        self.code = kwargs.get("code", self.get_code())
        template_param = '{"code":"%s"}' % self.code
        return template_param

