#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/3/11 17:52
# @Author   : 冉勇
# @File     : test_autaccess_token.py
# @Software : PyCharm
# @Desc     : 权限管理
import pytest
from fastapi.testclient import TestClient
from apps.vadmin.auth.views import app
from fastapi import status

# 模拟认证
app.dependency_overrides = {}

# 定义一个假的token
test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNTAyMDIyMTAxMCIsInBhc3N3b3JkIjoiJDJiJDEyJENlN2VTVUtJSWw4RE1LZUR5Tkh5ci5EcDRhZXNRQ003MFJlUGlnUlZFbnkxRXFsMzFSMENxIiwiZXhwIjoxNzEwMzExNjMxfQ.hOBOHLt4e2uTYAGyVcUKKr9X0w84f6Lx8--fwHoGkNo"


def test_get_user(test_client):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = test_client.get("/users", headers=headers)
    assert response.status_code == status.HTTP_200_OK


def test_create_user(test_client):
    headers = {"Authorization": f"Bearer {test_token}"}
    # todo: 写一个随机手机号hook或者一个硬删除接口
    data = {
        "name": "test001",
        "telephone": "13333333333",
        "email": "test@example.com",
        "nickname": "测试001",
        "avatar": "",
        "is_active": "true",
        "is_staff": "true",
        "gender": "0",
        "is_wx_server_openid": "false",
        "role_ids": [],
        "dept_ids": [],
        "password": ""
    }
    response = test_client.post("/users", headers=headers, json=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.fixture
def test_client():
    client = TestClient(app)
    return client
