# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/19 15:47
# @File           : production.py
# @IDE            : PyCharm
# @desc           : 数据库开发配置文件


"""
MongoDB 数据库配置

与接口是同一个数据库
"""
MONGO_DB_NAME = "数据库名称"
MONGO_DB_URL = f"mongodb://用户名:密码@地址:端口/?authSource={MONGO_DB_NAME}"


"""
Redis 数据库配置

与接口是同一个数据库
"""
REDIS_DB_URL = "redis://:密码@地址:端口/数据库名称"
