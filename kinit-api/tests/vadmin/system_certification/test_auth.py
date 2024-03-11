#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/3/11 17:52
# @Author   : 冉勇
# @File     : test_auth.py
# @Software : PyCharm
# @Desc     : 系统认证
from fastapi.testclient import TestClient
from apps.vadmin.auth.utils.login import app

client = TestClient(app)


def test_login():
    login_data = {
        "username ": "15020221010",
        "password": "kinit2022"
    }
    response = client.post("/auth/api/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    # 或者是否包含了某种形式的错误消息（取决于你的应用逻辑）
    # assert response.json() == {"detail": "Invalid credentials"}
