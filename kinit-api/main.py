# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/19 15:47
# @File           : main.py
# @IDE            : PyCharm
# @desc           : 主程序入口

from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from application import settings
from application import urls
from starlette.staticfiles import StaticFiles  # 依赖安装：pip install aiofiles
import importlib
from core.logger import logger
from core.exception import register_exception

"""
其他配置：
docs_url：配置交互文档的路由地址，如果禁用则为None，默认为 /docs
redoc_url： 配置 Redoc 文档的路由地址，如果禁用则为None，默认为 /redoc
openapi_url：配置接口文件json数据文件路由地址，如果禁用则为None，默认为/openapi.json
"""
app = FastAPI(
    title="KInit",
    description="初始项目，故事来源于，有一次我去面试，当时面试官给的一道题是让我使用Django+Vue写出一个客户信息列表的CRUD，"
                "里面给出的信息还是蛮复杂的，当时写了接近一下午，最后还没过，哈哈哈哈。写现在的这个初始项目也是为了真的再次遇到这种情况，"
                "我就可以很好的很快速的完成了。也能当领导安排新的项目，能够及时启动项目，不用再搭建脚手架了。",
    version="1.0.0",
)

"""
添加中间件
"""
for middle in settings.MIDDLEWARES:
    try:
        # 动态导入模块
        middle_pag = importlib.import_module(middle[0:middle.rindex(".")])
        getattr(middle_pag, middle[middle.rindex(".")+1:])(app)
    except ModuleNotFoundError:
        logger.error(f"AttributeError：导入中间件失败，未找到该模块：{middle}")
    except AttributeError:
        logger.error(f"ModuleNotFoundError：导入中间件失败，未找到该模块下的方法：{middle}")

"""
全局异常捕捉处理
"""
register_exception(app)

"""
跨域解决
"""
if settings.CORS_ORIGIN_ENABLE:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS)

"""
挂在静态目录
"""
if settings.STATIC_ENABLE:
    app.mount(settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT))

"""
引入应用中的路由
"""
for url in urls.urlpatterns:
    app.include_router(url["ApiRouter"], prefix=url["prefix"], tags=url["tags"])

if __name__ == '__main__':
    """
    # 启动项目
    # reload：自动重载项目
    # debug：调试
    # workers：启动几个进程
    """
    uvicorn.run(app='main:app', host="0.0.0.0", port=9000, reload=True, debug=True, workers=1)
