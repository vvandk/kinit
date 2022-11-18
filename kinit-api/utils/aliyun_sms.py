# -*- coding: utf-8 -*-
# @version        : 1.3
# @Creaet Time    : 2021/3/15
# @Author         : LZK
# @File           : aliyun_sms.py
# @Software       : PyCharm
# @Update Time    : 2022/11/08
# @Title          : 最新版阿里云短信服务发送程序（Python版本）2022-11-08


"""
短信 API 官方文档：https://help.aliyun.com/document_detail/419298.html?spm=5176.25163407.help.dexternal.6ff2bb6ercg9x3
发送短信 官方文档：https://help.aliyun.com/document_detail/419273.htm?spm=a2c4g.11186623.0.0.36855d7aRBSwtP
Python SDK 官方文档：https://help.aliyun.com/document_detail/215764.html?spm=a2c4g.11186623.0.0.6a0c4198XsBJNW

环境要求
Python 3
安装 SDK 核心库 OpenAPI ，使用pip安装包依赖:
pip install alibabacloud_tea_openapi
pip install alibabacloud_dysmsapi20170525
"""
import json
import random
import re
from enum import Enum, unique
from core.exception import CustomException
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from core.logger import logger
import datetime
from aioredis.client import Redis
from utils.cache import cache_aliyun_settings
from utils import status


class AliyunSMS:

    # 返回错误码对应：
    doc = "https://help.aliyun.com/document_detail/101346.html"

    @unique
    class Scene(Enum):
        login = "sms_template_code_1"
        reset_password = "sms_template_code_2"

    def __init__(self, rd: Redis, telephone: str):
        self.check_telephone_format(telephone)
        self.telephone = telephone
        self.rd = rd
        self.code = None
        self.scene = None

    async def __get_settings(self, number: int = 3):
        """
        获取配置信息
        """
        aliyun_sms = await self.rd.get("aliyun_sms")
        if not aliyun_sms and number > 0:
            logger.error(f"未从Redis中获取到短信配置信息，正在重新更新配置信息，重试次数：{number}")
            await cache_aliyun_settings(self.rd)
            await self.__get_settings(number - 1)
        elif not aliyun_sms and number:
            raise CustomException("获取短信配置信息失败，请联系管理员！", code=status.HTTP_ERROR)
        else:
            aliyun_sms = json.loads(aliyun_sms)
            self.access_key = aliyun_sms.get("sms_access_key")
            self.access_key_secret = aliyun_sms.get("sms_access_key_secret")
            self.send_interval = int(aliyun_sms.get("sms_send_interval"))
            self.valid_time = int(aliyun_sms.get("sms_valid_time"))
            if self.scene == self.Scene.login:
                self.sign_name = aliyun_sms.get("sms_sign_name_1")
            else:
                self.sign_name = aliyun_sms.get("sms_sign_name_2")
            self.template_code = aliyun_sms.get(self.scene.value)

    async def main_async(self, scene: Scene, **kwargs) -> bool:
        """
        主程序入口，异步方式
        """
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if await self.rd.get(self.telephone + "_flag_"):
            logger.error(f'{send_time} {self.telephone} 短信发送失败，短信发送过于频繁')
            print(f"{self.telephone} 短信发送频繁")
            raise CustomException(msg="短信发送频繁", code=status.HTTP_ERROR)
        self.scene = scene
        await self.__get_settings()
        return await self.__send(**kwargs)

    async def __send(self, **kwargs) -> bool:
        """
        发送短信
        """
        client = self.create_client(self.access_key, self.access_key_secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=self.telephone,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=self.__get_template_param(**kwargs)
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = await client.send_sms_with_options_async(send_sms_request, runtime)
            return await self.__validation(resp)
        except Exception as e:
            print(e.__str__())
            return False

    def __get_template_param(self, **kwargs) -> str:
        """
        获取模板参数
        """
        if self.scene == self.Scene.login:
            self.code = kwargs.get("code", self.get_code())
            template_param = '{"code":"%s"}' % self.code
        elif self.scene == self.Scene.reset_password:
            self.code = kwargs.get("password")
            template_param = '{"password":"%s"}' % self.code
        else:
            raise CustomException(msg="获取发送场景失败", code=status.HTTP_ERROR)
        return template_param

    async def __validation(self, resp: dysmsapi_20170525_models.SendSmsResponse) -> bool:
        """
        验证结果并返回
        """
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if resp.body.code == "OK":
            logger.info(f'{send_time} {self.telephone} 短信发送成功，返回code：{resp.body.code}')
            await self.rd.set(self.telephone, self.code, self.valid_time)
            await self.rd.set(self.telephone + "_flag_", self.code, self.send_interval)
            return True
        else:
            logger.error(f'{send_time} {self.telephone} 短信发送失败，返回code：{resp.body.code}，请参考文档：{self.doc}')
            return False

    async def check_sms_code(self, code: str) -> bool:
        """
        检查短信验证码是否正确
        """
        if code and code == await self.rd.get(self.telephone):
            await self.rd.delete(self.telephone)
            await self.rd.delete(self.telephone + "_flag_")
            return True
        return False

    @staticmethod
    def get_code(length: int = 6, blend: bool = False) -> str:
        """
        随机获取短信验证码
        短信验证码只支持数字，不支持字母及其他符号

        @param length: 验证码长度
        @param blend: 是否 字母+数字 混合
        """
        code = ""  # 创建字符串变量,存储生成的验证码
        for i in range(length):  # 通过for循环控制验证码位数
            num = random.randint(0, 9)  # 生成随机数字0-9
            if blend:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
                upper_alpha = chr(random.randint(65, 90))
                lower_alpha = chr(random.randint(97, 122))
                # 随机选择其中一位
                num = random.choice([num, upper_alpha, lower_alpha])
            code = code + str(num)
        return code

    @staticmethod
    def check_telephone_format(telephone: str) -> bool:
        """
        检查手机号格式是否合法
        """
        REGEX_TELEPHONE = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'

        if not telephone:
            raise CustomException(msg="手机号码不能为空", code=400)
        elif not re.match(REGEX_TELEPHONE, telephone):
            raise CustomException(msg="手机号码格式不正确", code=400)
        return True

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的 AccessKey ID,
            access_key_id=access_key_id,
            # 您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

