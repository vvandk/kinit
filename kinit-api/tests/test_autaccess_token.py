#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/3/12 14:13
# @Author   : 冉勇
# @File     : test_autaccess_token.py
# @Software : PyCharm
# @Desc     :
import unittest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from apps.vadmin.auth.utils.login import app
from apps.vadmin.auth.models import VadminUser


class TestLoginAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('apps.vadmin.auth.crud.UserDal.get_data')
    async def test_api_login_for_access_token(self, mock_get_data):
        # 模拟数据库返回的用户数据
        mock_user = VadminUser(
            telephone='15020221010', password='$2b$12$Ce7eSUKIIl8DMKeDyNHyr.Dp4aesQCM70RePigRVEny1Eql31R0Cq',
            is_active=True, is_staff=True
        )
        mock_get_data.return_value = mock_user

        # 发送登录请求
        response = self.client.post(
            '/api/login', data={'username': '15020221010', 'password': 'kinit2022'}
        )

        # 断言响应状态码
        self.assertEqual(response.status_code, 200)

        # 断言响应数据
        data = response.json()
        print(data)
        self.assertIn('access_token', data)
        self.assertEqual(data['token_type'], 'bearer')


if __name__ == '__main__':
    unittest.main()
