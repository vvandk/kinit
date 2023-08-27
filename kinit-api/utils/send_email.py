#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/3/27 9:48 
# @File           : send_email.py
# @IDE            : PyCharm
# @desc           : 发送邮件封装类


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List
from redis.asyncio import Redis

from core.exception import CustomException
from utils.cache import Cache


class EmailSender:

    def __init__(self, rd: Redis):
        self.email = None
        self.password = None
        self.smtp_server = None
        self.smtp_port = None
        self.server = None
        self.rd = rd

    async def __get_settings(self, retry: int = 3):
        """
        获取配置信息
        """
        web_email = await Cache(self.rd).get_tab_name("web_email", retry)
        self.email = web_email.get("email_access")
        self.password = web_email.get("email_password")
        self.smtp_server = web_email.get("email_server")
        self.smtp_port = int(web_email.get("email_port"))

        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()
        try:
            self.server.login(self.email, self.password)
        except smtplib.SMTPAuthenticationError:
            raise CustomException("邮件发送失败，邮箱服务器认证失败！")
        except AttributeError:
            raise CustomException("邮件发送失败，邮箱服务器认证失败！")

    async def send_email(self, to_emails: List[str], subject: str, body: str, attachments: List[str] = None):
        """
        发送邮件
        :param to_emails: 收件人，一个或多个
        :param subject: 主题
        :param body: 内容
        :param attachments: 附件
        """
        await self.__get_settings()

        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = ', '.join(to_emails)
        message['Subject'] = subject
        body = MIMEText(body)
        message.attach(body)
        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as f:
                    file_data = f.read()
                filename = attachment.split('/')[-1]
                attachment = MIMEApplication(file_data, Name=filename)
                attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
                message.attach(attachment)
        try:
            result = self.server.sendmail(self.email, to_emails, message.as_string())
            self.server.quit()
            print("邮件发送结果", result)
            if result:
                return False
            else:
                return True
        except smtplib.SMTPException as e:
            self.server.quit()
            print('邮件发送失败！错误信息：', e)
            return False


# if __name__ == '__main__':
#     sender = EmailSender()
#     to_emails = ['ktianc2001@163.com', '2445667550@qq.com']
#     subject = 'Test email'
#     body = 'This is a test email'
#     sender.send_email(to_emails, subject, body)
