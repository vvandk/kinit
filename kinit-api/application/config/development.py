# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/19 15:47
# @File           : development.py
# @IDE            : PyCharm
# @desc           : 数据库生产配置文件


"""
Mysql 数据库配置项
连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
"""
SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@177.8.0.7:3306/kinit"


"""
Redis 数据库配置
格式："redis://:密码@地址:端口/数据库名称"
"""
REDIS_DB_ENABLE = True
REDIS_DB_URL = "redis://:123456@177.8.0.5:6379/1"

"""
MongoDB 数据库配置
格式：mongodb://用户名:密码@地址:端口/?authSource=数据库名称
"""
MONGO_DB_ENABLE = True
MONGO_DB_NAME = "kinit"
MONGO_DB_URL = f"mongodb://kinit:123456@177.8.0.6:27017/?authSource={MONGO_DB_NAME}"


"""
阿里云对象存储OSS配置
阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
 *  [accessKeyId] {String}：通过阿里云控制台创建的AccessKey。
 *  [accessKeySecret] {String}：通过阿里云控制台创建的AccessSecret。
 *  [bucket] {String}：通过控制台或PutBucket创建的bucket。
 *  [endpoint] {String}：bucket所在的区域， 默认oss-cn-hangzhou。
"""
ALIYUN_OSS = {
    "accessKeyId": "accessKeyId",
    "accessKeySecret": "accessKeySecret",
    "endpoint": "endpoint",
    "bucket": "bucket",
    "baseUrl": "baseUrl"
}

"""
获取IP地址归属地
文档：https://user.ip138.com/ip/doc
"""
IP_PARSE_ENABLE = False
IP_PARSE_TOKEN = "IP_PARSE_TOKEN"
