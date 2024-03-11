#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/3/11 17:04
# @Author   : 冉勇
# @File     : test_test.py
# @Software : PyCharm
# @Desc     :
from fastapi.testclient import TestClient
from apps.vadmin.auth.views import app

client = TestClient(app)


def test_test():
    response = client.get("/test")
    assert response.status_code == 200
