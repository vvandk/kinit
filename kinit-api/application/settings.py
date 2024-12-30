# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/19 15:47
# @File           : settings.py
# @IDE            : PyCharm
# @desc           : 主配置文件

import os
from fastapi.security import OAuth2PasswordBearer

"""
系统版本
"""
VERSION = "3.10.1"

"""安全警告: 不要在生产中打开调试运行!"""
DEBUG = True

"""是否开启演示功能：取消所有POST,DELETE,PUT操作权限"""
DEMO = False
"""演示功能白名单"""
DEMO_WHITE_LIST_PATH = [
    "/auth/login",
    "/auth/token/refresh",
    "/auth/wx/login",
    "/vadmin/system/dict/types/details",
    "/vadmin/system/settings/tabs",
    "/vadmin/resource/images",
    "/vadmin/auth/user/export/query/list/to/excel"
]
"""演示功能黑名单（触发异常 status_code=403），黑名单优先级更高"""
DEMO_BLACK_LIST_PATH = [
    "/auth/api/login"
]

"""
引入数据库配置
"""
if DEBUG:
    from application.config.development import *
else:
    from application.config.production import *

"""项目根目录"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""
是否开启登录认证
只适用于简单的接口
如果是与认证关联性比较强的接口，则无法使用
"""
OAUTH_ENABLE = True
"""
配置 OAuth2 密码流认证方式
官方文档：https://fastapi.tiangolo.com/zh/tutorial/security/first-steps/#fastapi-oauth2passwordbearer
auto_error:(bool) 可选参数，默认为 True。当验证失败时，如果设置为 True，FastAPI 将自动返回一个 401 未授权的响应，如果设置为 False，你需要自己处理身份验证失败的情况。
这里的 auto_error 设置为 False 是因为存在 OpenAuth：开放认证，无认证也可以访问，
如果设置为 True，那么 FastAPI 会自动报错，即无认证时 OpenAuth 会失效，所以不能使用 True。
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/api/login", auto_error=False) if OAUTH_ENABLE else lambda: ""
"""安全的随机密钥，该密钥将用于对 JWT 令牌进行签名"""
SECRET_KEY = 'vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=kbvqacjq75vzps$'
"""用于设定 JWT 令牌签名算法"""
ALGORITHM = "HS256"
"""access_token 过期时间，一天"""
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
"""refresh_token 过期时间，用于刷新token使用，两天"""
REFRESH_TOKEN_EXPIRE_MINUTES = 1440 * 2
"""access_token 缓存时间，用于刷新token使用，30分钟"""
ACCESS_TOKEN_CACHE_MINUTES = 30

"""
挂载临时文件目录，并添加路由访问，此路由不会在接口文档中显示
TEMP_DIR：临时文件目录绝对路径
官方文档：https://fastapi.tiangolo.com/tutorial/static-files/
"""
TEMP_DIR = os.path.join(BASE_DIR, "temp")

"""
挂载静态目录，并添加路由访问，此路由不会在接口文档中显示
STATIC_ENABLE：是否启用静态目录访问
STATIC_URL：路由访问
STATIC_ROOT：静态文件目录绝对路径
官方文档：https://fastapi.tiangolo.com/tutorial/static-files/
"""
STATIC_ENABLE = True
STATIC_URL = "/media"
STATIC_DIR = "static"
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_DIR)


"""
跨域解决
详细解释：https://cloud.tencent.com/developer/article/1886114
官方文档：https://fastapi.tiangolo.com/tutorial/cors/
"""
# 是否启用跨域
CORS_ORIGIN_ENABLE = True
# 只允许访问的域名列表，* 代表所有
ALLOW_ORIGINS = ["*"]
# 是否支持携带 cookie
ALLOW_CREDENTIALS = True
# 设置允许跨域的http方法，比如 get、post、put等。
ALLOW_METHODS = ["*"]
# 允许携带的headers，可以用来鉴别来源等作用。
ALLOW_HEADERS = ["*"]

"""
全局事件配置
"""
EVENTS = [
    "core.event.connect_mongo" if MONGO_DB_ENABLE else None,
    "core.event.connect_redis" if REDIS_DB_ENABLE else None,
]

"""
其他项目配置
"""
# 默认密码，"0" 默认为手机号后六位
DEFAULT_PASSWORD = "0"
# 默认头像
DEFAULT_AVATAR = "https://vv-reserve.oss-cn-hangzhou.aliyuncs.com/avatar/2023-01-27/1674820804e81e7631.png"
# 默认登陆时最大输入密码或验证码错误次数
DEFAULT_AUTH_ERROR_MAX_NUMBER = 5
# 是否开启保存登录日志
LOGIN_LOG_RECORD = True
# 是否开启保存每次请求日志到本地
REQUEST_LOG_RECORD = True
# 是否开启每次操作日志记录到MongoDB数据库
OPERATION_LOG_RECORD = True
# 只记录包括的请求方式操作到MongoDB数据库
OPERATION_RECORD_METHOD = ["POST", "PUT", "DELETE"]
# 忽略的操作接口函数名称，列表中的函数名称不会被记录到操作日志中
IGNORE_OPERATION_FUNCTION = ["post_dicts_details"]

"""
中间件配置
"""
MIDDLEWARES = [
    "core.middleware.register_request_log_middleware" if REQUEST_LOG_RECORD else None,
    "core.middleware.register_operation_record_middleware" if OPERATION_LOG_RECORD and MONGO_DB_ENABLE else None,
    "core.middleware.register_demo_env_middleware" if DEMO else None,
    "core.middleware.register_jwt_refresh_middleware"
]

"""
定时任务配置
"""
# 发布/订阅通道，与定时任务程序相互关联，请勿随意更改
SUBSCRIBE = 'kinit_queue'
