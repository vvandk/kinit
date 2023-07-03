# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/19 15:47
# @File           : middleware.py
# @IDE            : PyCharm
# @desc           : 中间件

"""
官方文档——中间件：https://fastapi.tiangolo.com/tutorial/middleware/
官方文档——高级中间件：https://fastapi.tiangolo.com/advanced/middleware/
"""
import datetime
import json
import time
from fastapi import Request, Response
from core.logger import logger
from fastapi import FastAPI
from fastapi.routing import APIRoute
from user_agents import parse
from application.settings import OPERATION_RECORD_METHOD, MONGO_DB_ENABLE, IGNORE_OPERATION_FUNCTION,\
    DEMO_WHITE_LIST_PATH, DEMO
from utils.response import ErrorResponse
from apps.vadmin.record.crud import OperationRecordDal
from core.database import mongo_getter


def write_request_log(request: Request, response: Response):
    http_version = f"http/{request.scope['http_version']}"
    content_length = response.raw_headers[0][1]
    process_time = response.headers["X-Process-Time"]
    content = f"basehttp.log_message: '{request.method} {request.url} {http_version}' {response.status_code}" \
              f"{response.charset} {content_length} {process_time}"
    logger.info(content)


def register_request_log_middleware(app: FastAPI):
    """
    记录请求日志中间件
    :param app:
    :return:
    """

    @app.middleware("http")
    async def request_log_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        write_request_log(request, response)
        return response


def register_operation_record_middleware(app: FastAPI):
    """
    操作记录中间件
    用于将使用认证的操作全部记录到 mongodb 数据库中
    :param app:
    :return:
    """

    @app.middleware("http")
    async def operation_record_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        if not MONGO_DB_ENABLE:
            return response
        telephone = request.scope.get('telephone', None)
        user_id = request.scope.get('user_id', None)
        user_name = request.scope.get('user_name', None)
        route = request.scope.get('route')
        if not telephone:
            return response
        elif request.method not in OPERATION_RECORD_METHOD:
            return response
        elif route.name in IGNORE_OPERATION_FUNCTION:
            return response
        process_time = time.time() - start_time
        user_agent = parse(request.headers.get("user-agent"))
        system = f"{user_agent.os.family} {user_agent.os.version_string}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        query_params = dict(request.query_params.multi_items())
        path_params = request.path_params
        if isinstance(request.scope.get('body'), str):
            body = request.scope.get('body')
        else:
            body = request.scope.get('body').decode()
            if body:
                body = json.loads(body)
        params = {
            "body": body,
            "query_params": query_params if query_params else None,
            "path_params": path_params if path_params else None,
        }
        content_length = response.raw_headers[0][1]
        assert isinstance(route, APIRoute)
        document = {
            "process_time": process_time,
            "telephone": telephone,
            "user_id": user_id,
            "user_name": user_name,
            "request_api": request.url.__str__(),
            "client_ip": request.client.host,
            "system": system,
            "browser": browser,
            "request_method": request.method,
            "api_path": route.path,
            "summary": route.summary,
            "description": route.description,
            "tags": route.tags,
            "route_name": route.name,
            "status_code": response.status_code,
            "content_length": content_length,
            "create_datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "params": json.dumps(params)
        }
        await OperationRecordDal(mongo_getter(request)).create_data(document)
        return response


def register_demo_env_middleware(app: FastAPI):
    """
    演示环境中间件
    :param app:
    :return:
    """

    @app.middleware("http")
    async def demo_env_middleware(request: Request, call_next):
        path = request.scope.get("path")
        if request.method != "GET":
            print("路由：", path, request.method)
        if DEMO and request.method != "GET" and path not in DEMO_WHITE_LIST_PATH:
            return ErrorResponse(msg="演示环境，禁止操作")
        return await call_next(request)


def register_jwt_refresh_middleware(app: FastAPI):
    """
    JWT刷新中间件
    :param app:
    :return:
    """

    @app.middleware("http")
    async def jwt_refresh_middleware(request: Request, call_next):
        response = await call_next(request)
        refresh = request.scope.get('if-refresh', 0)
        response.headers["if-refresh"] = str(refresh)
        return response
