# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/19 15:47
# @File           : middleware.py
# @IDE            : PyCharm
# @desc           : 中间件

"""
官方文档——中间件：https://fastapi.tiangolo.com/tutorial/middleware/
官方文档——高级中间件：https://fastapi.tiangolo.com/advanced/middleware/
"""


import time
from fastapi import Request, Response
from core.logger import logger
from fastapi import FastAPI


# 记录请求日志
def write_request_log(request: Request, response: Response):
    http_version = f"http/{request.scope['http_version']}"
    content_length = response.raw_headers[0][1]
    process_time = response.headers["X-Process-Time"]
    content = f"basehttp.log_message: '{request.method} {request.url} {http_version}' {response.status_code} {response.charset} {content_length} {process_time}"
    logger.info(content)


def register_middleware(app: FastAPI):
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
