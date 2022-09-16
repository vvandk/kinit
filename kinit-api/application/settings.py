# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/19 15:47
# @File           : settings.py
# @IDE            : PyCharm
# @desc           : 主配置文件

import os
from fastapi.security import OAuth2PasswordBearer

# 安全警告: 不要在生产中打开调试运行!
DEBUG = True

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMP_DIR = os.path.join(BASE_DIR, "temp")

"""是否开启登录认证"""
OAUTH_ENABLE = True
"""登录认证视图"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/", auto_error=False) if OAUTH_ENABLE else lambda: ""
"""安全的随机密钥，该密钥将用于对 JWT 令牌进行签名"""
SECRET_KEY = 'vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=kbvqacjq75vzps$'
"""用于设定 JWT 令牌签名算法"""
ALGORITHM = "HS256"
"""令牌过期时间，9999分钟"""
ACCESS_TOKEN_EXPIRE_MINUTES = 9999

"""安全的随机密钥，该密钥将用于对校区标识进行签名"""
SYSTEM_KEY = "0CoJUm6Qywm6ts68"

"""
挂载静态目录，并添加路由访问，此路由不会在接口文档中显示
STATIC_ENABLE：是否启用静态目录
STATIC_URL：路由访问
STATIC_ROOT：静态文件目录相对路径
官方文档：https://fastapi.tiangolo.com/tutorial/static-files/
"""
STATIC_ENABLE = True
STATIC_URL = "/static"
STATIC_ROOT = "./static"


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
数据库配置项
连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
"""
if DEBUG:
    # 测试库
    SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:Ktianc123@rm-bp181adf0phw2o0r05o.mysql.rds.aliyuncs.com:3306/kinit"
    SQLALCHEMY_DATABASE_TYPE = "mysql"
else:
    # 正式库
    SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:Ktianc123@rm-bp181adf0phw2o0r05o.mysql.rds.aliyuncs.com:3306/kinit"
    SQLALCHEMY_DATABASE_TYPE = "mysql"


"""
中间件配置
"""
MIDDLEWARES = [
    "core.middleware.register_middleware",
]

"""
默认配置
"""
# 默认密码，"0" 默认为手机号后六位
DEFAULT_PASSWORD = "0"
