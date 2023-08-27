#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/6/14 15:26 
# @File           : aliyun.py
# @IDE            : PyCharm
# @desc           : 最新版阿里云短信服务发送程序（Python版本）2022-11-08

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
import random
import re
from typing import List
from core.exception import CustomException
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from core.logger import logger
import datetime
from redis.asyncio.client import Redis
from utils.cache import Cache
from utils.db_getter import DBGetter


class AliyunSMS(DBGetter):
    # 返回错误码对应：
    doc = "https://help.aliyun.com/document_detail/101346.html"

    def __init__(self, telephones: List[str], rd: Redis = None):
        super().__init__()
        self.check_telephones_format(telephones)
        self.telephones = telephones
        self.rd = rd

        self.sign_conf = None  # 数据库中 sms_sign_name_* 的配置
        self.template_code_conf = None  # 数据库中 sms_template_code_* 的配置
        # 以上两个配置项的好处在于可以灵活配置短信信息，不需要改代码

    async def main_async(self, **kwargs) -> List[bool]:
        """
        主程序入口，异步方式

        redis 对象必填
        """
        result = []
        await self._get_settings_async()
        for telephone in self.telephones:
            result.append(await self._send_async(telephone, **kwargs))
        return result

    async def _send_async(self, telephone: str, **kwargs) -> bool:
        """
        发送短信
        """
        client = self.create_client(self.access_key, self.access_key_secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=telephone,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=self._get_template_param(**kwargs)
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = await client.send_sms_with_options_async(send_sms_request, runtime)
            return self._validation(telephone, resp)
        except Exception as e:
            print(e.__str__())
            return False

    async def _get_settings_async(self, retry: int = 3):
        """
        获取配置信息
        """
        if not self.rd:
            raise ValueError("缺少 redis 对象参数！")
        elif not self.sign_conf or not self.template_code_conf:
            raise ValueError("缺少短信签名信息和短信模板ID！")
        aliyun_sms = await Cache(self.rd).get_tab_name("aliyun_sms", retry)
        self.access_key = aliyun_sms.get("sms_access_key")
        self.access_key_secret = aliyun_sms.get("sms_access_key_secret")
        self.send_interval = int(aliyun_sms.get("sms_send_interval"))
        self.valid_time = int(aliyun_sms.get("sms_valid_time"))
        self.sign_name = aliyun_sms.get(self.sign_conf)
        self.template_code = aliyun_sms.get(self.template_code_conf)

    def main(self, **kwargs) -> List[bool]:
        """
        主程序入口，同步方式
        """
        result = []
        self._get_settings()
        for telephone in self.telephones:
            result.append(self._send(telephone, **kwargs))
        return result

    def _send(self, telephone: str, **kwargs) -> bool:
        """
        同步方式发送短信
        """
        client = self.create_client(self.access_key, self.access_key_secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=telephone,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=self._get_template_param(**kwargs)
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = client.send_sms_with_options(send_sms_request, runtime)
            return self._validation(telephone, resp)
        except Exception as e:
            print(e.__str__())
            return False

    def _get_settings(self):
        """
        同步方式获取配置信息
        """
        if not self.sign_conf or not self.template_code_conf:
            raise ValueError("缺少短信签名信息和短信模板ID！")
        self.conn_mysql()
        sql = f"""
        SELECT
            config_value 
        FROM
            `vadmin_system_settings` 
        WHERE
            config_key IN (
                'sms_access_key',
                'sms_access_key_secret',
                'sms_send_interval',
                'sms_valid_time',
                '{self.sign_conf}',
                '{self.template_code_conf}'
            )
        """
        self.mysql_cursor.execute(sql)
        result = self.mysql_cursor.fetchall()
        self.close_mysql()
        self.access_key = result[0][0]
        self.access_key_secret = result[1][0]
        self.send_interval = result[2][0]
        self.valid_time = result[3][0]
        self.sign_name = result[4][0]
        self.template_code = result[5][0]

    def _get_template_param(self, **kwargs) -> str:
        """
        获取模板参数

        可以被子类继承的受保护的私有方法
        """
        raise NotImplementedError("该方法应该被重写！")

    def _validation(self, telephone: str, resp: dysmsapi_20170525_models.SendSmsResponse) -> bool:
        """
        验证结果并返回
        """
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if resp.body.code == "OK":
            logger.info(f'{send_time} {telephone} 短信发送成功，返回code：{resp.body.code}')
            return True
        else:
            logger.error(f'{send_time} {telephone} 短信发送失败，返回code：{resp.body.code}，请参考文档：{self.doc}')
            return False

    @staticmethod
    def get_code(length: int = 6, blend: bool = False) -> str:
        """
        随机获取短信验证码
        短信验证码只支持数字，不支持字母及其他符号

        :param length: 验证码长度
        :param blend: 是否 字母+数字 混合
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

    @classmethod
    def check_telephones_format(cls, telephones: List[str]) -> bool:
        """
        同时检查多个手机号格式是否合法

        不合法就会抛出异常
        """
        for telephone in telephones:
            cls.check_telephone_format(telephone)
        return True

    @staticmethod
    def check_telephone_format(telephone: str) -> bool:
        """
        检查手机号格式是否合法

        不合法就会抛出异常
        """
        REGEX_TELEPHONE = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'

        if not telephone:
            raise CustomException(msg=f"手机号码（{telephone}）不能为空", code=400)
        elif not re.match(REGEX_TELEPHONE, telephone):
            raise CustomException(msg=f"手机号码（{telephone}）格式不正确", code=400)
        return True

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        :param access_key_id:
        :param access_key_secret:
        :return: Client
        :throws Exception
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
