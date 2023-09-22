<div align="center">
    <p align="center">
        <img src="https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/logo.png" height="150" alt="logo"/>
    </p>
</div>




## [关于]

<div align="center"><h3 align="center">Kinit 是一套开箱即用的中后台解决方案，可以作为新项目的启动模版！</h3></div>
<div align="center"><h3 align="center">前后端分离架构，开箱即用，紧随前沿技术！</h3></div>

<div align="center"><h3 align="center">高性能，高效率，高颜值，易扩展</h3></div>

<div align="center"><h3 align="center">长期维护，积极更新！</h3></div>

## 介绍

Kinit 是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。

- 后端采用现代、快速（高性能） [FastAPI](https://fastapi.tiangolo.com/zh/) 异步框架 + 自动生成交互式API文档 + （强制类型约束）[Pydantic](https://docs.pydantic.dev/1.10/) + （高效率）[SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/index.html)；
- PC端采用 [vue-element-plus-admin 2.2.0](https://gitee.com/kailong110120130/vue-element-plus-admin) 、[Vue3](https://cn.vuejs.org/guide/introduction.html)、[Element Plus](https://element-plus.gitee.io/zh-CN/guide/design.html)、[TypeScript](https://www.tslang.cn/)等主流技术开发；
- 移动端采用 [uni-app](https://uniapp.dcloud.net.cn/component/)，[Vue2](https://v2.cn.vuejs.org/v2/guide/)，[uView 2](https://www.uviewui.com/components/intro.html)为主要技术开发；
- 后端加入 [Typer](https://typer.tiangolo.com/) 命令行应用，简单化数据初始化，数据表模型迁移等操作；
- 已加入定时任务功能，采用 [APScheduler](https://github.com/agronholm/apscheduler) 定时任务框架 + [Redis](https://redis.io/)  消息队列 + [MongoDB](https://www.mongodb.com/) 持久存储；
- 权限认证使用[（哈希）密码和 JWT Bearer 令牌的 OAuth2](https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/)，支持多终端认证系统。
- 支持加载动态权限菜单，多方式轻松权限控制，按钮级别权限控制。
- 已加入常见的 [MySQL](https://www.mysql.com/) + [MongoDB](https://www.mongodb.com/) + [Redis](https://redis.io/)  数据库异步操作。
- 支持 [docker-compose](https://docs.docker.com/compose/) 部署方式
- 开箱即用的中后台解决方案，可以用来作为新项目的启动模版，也可用于学习参考。并且时刻关注着最新技术动向，尽可能的第一时间更新。
- 与 [vue-element-plus-admin](https://gitee.com/kailong110120130/vue-element-plus-admin) 前端框架时刻保持同步更新。

## 特别鸣谢

[vue-element-plus-admin](https://gitee.com/kailong110120130/vue-element-plus-admin)：基于vue3、element-plus、typescript 的后台集成方案

[RuoYi 若依官方网站](http://www.ruoyi.vip/)：RuoYi 是一个优秀的 Java 后台管理系统

[django-vue-admin](https://gitee.com/liqianglog/django-vue-admin)：django-vue-admin 是一个优秀的基于 Django 开发后台管理系统

[小诺开源技术 (xiaonuo.vip)](https://www.xiaonuo.vip/)：国内首个国密前后端分离快速开发平台

## 在线体验

PC端演示地址：https://kinit.ktianc.top

微信小程序端演示：

- 搜索：kinit
- 扫码：

<div align="center">
    <p align="center">
        <img src="https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/gh_5566dcf85bf0_860.jpg" height="150" alt="logo"/>
    </p>
</div>


- 账号：15020221010
- 密码：kinit2022

## 源码地址

gitee地址(主推)：https://gitee.com/ktianc/kinit

github地址：https://github.com/vvandk/kinit

## PC端内置功能

- [x] 菜单管理：配置系统菜单，操作权限，按钮权限标识、后端接口权限等。

- [x] 角色管理：角色菜单权限分配。

- [x] 用户管理：用户是系统操作者，该功能主要完成系统用户配置。

- [x] 个人主页：配置用户个人信息，密码修改等。

- [x] 字典管理：对系统中经常使用的一些较为固定的数据进行维护。

- [x] 文件上传：对接阿里云OSS与本地存储。

- [x] 登录认证：目前支持用户使用手机号+密码登录方式，手机验证码登录方式。

  说明：新建用户密码默认为手机号后六位；

  说明：用户在第一次登录时，必须修改当前用户密码。

- [x] 系统配置：对本系统环境信息进行动态配置

  网站标题，LOGO，描述，ICO，备案号，底部内容，微信小程序信息，等等

- [x] 用户分布：接入高德地图显示各地区用户分布情况

- [x] 数据概览：提供两种数据统计展示模板，更直观的查看数据统计情况

- [x] 智慧大屏：大屏展示`办公室空气质量实时检测`数据分析

- [x] 登录日志：用户登录日志记录和查询。

- [x] 操作日志：系统用户每次操作功能时的详细记录。

- [x] 接口文档：提供自动生成的交互式 API 文档，与 ReDoc 文档

- [x] 导入导出：灵活支持数据导入导出功能

- [x] 已加入常见的`Redis`、`MySQL`、`MongoDB`数据库异步操作。

- [x] 命令行操作：新加入 `Typer` 命令行应用，简单化数据初始化，数据表模型迁移。

- [x] 定时任务：在线操作（添加、修改、删除)任务调度包含查看任务执行结果日志。

## 移动端内置功能

- [x] 登录认证：支持用户使用手机号+密码方式登录，微信手机号一键登录方式。

  说明：新建用户密码默认为手机号后六位；

  说明：用户在第一次登录时，必须修改当前用户密码。

- [x] 导航栏：首页、我的、工作台

- [x] 我的基础功能：编辑资料、头像修改、密码修改、常见问题、关于我们等

##  前序准备

### 后端技术

- [Python3](https://www.python.org/downloads/windows/)：熟悉 python3 基础语法
- [FastAPI](https://fastapi.tiangolo.com/zh/) - 熟悉后台接口 Web 框架
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/index.html) - 数据数据库操作
- [Typer](https://typer.tiangolo.com/) - 熟悉命令行工具的使用
- [MySQL](https://www.mysql.com/) 和 [MongoDB](https://www.mongodb.com/) 和 [Redis](https://redis.io/)  - 熟悉数据存储数据库
- [iP查询接口文档](https://user.ip138.com/ip/doc)：IP查询第三方服务，有1000次的免费次数

### PC端

- [node](https://gitee.com/link?target=http%3A%2F%2Fnodejs.org%2F) 和 [git](https://gitee.com/link?target=https%3A%2F%2Fgit-scm.com%2F) - 项目开发环境
- [Vite](https://gitee.com/link?target=https%3A%2F%2Fvitejs.dev%2F) - 熟悉 vite 特性
- [Vue3](https://gitee.com/link?target=https%3A%2F%2Fv3.vuejs.org%2F) - 熟悉 Vue 基础语法
- [TypeScript](https://gitee.com/link?target=https%3A%2F%2Fwww.typescriptlang.org%2F) - 熟悉 `TypeScript` 基本语法
- [Es6+](https://gitee.com/link?target=http%3A%2F%2Fes6.ruanyifeng.com%2F) - 熟悉 es6 基本语法
- [Vue-Router-Next](https://gitee.com/link?target=https%3A%2F%2Fnext.router.vuejs.org%2F) - 熟悉 vue-router 基本使用
- [Element-Plus](https://gitee.com/link?target=https%3A%2F%2Felement-plus.org%2F) - element-plus 基本使用
- [vue3-json-viewer](https://gitee.com/isfive/vue3-json-viewer)：简单易用的json内容展示组件,适配vue3和vite。
- [高德地图API (amap.com)](https://lbs.amap.com/api/jsapi-v2/guide/webcli/map-vue1)：地图 JSAPI 2.0 是高德开放平台免费提供的第四代 Web 地图渲染引擎。

### 移动端

- [uni-app](https://uniapp.dcloud.net.cn/component/) - 熟悉 uni-app 基本语法
- [Vue2](https://v2.cn.vuejs.org/v2/guide/) - 熟悉 Vue 基础语法
- [uView UI 2](https://www.uviewui.com/components/intro.html)：uView UI 组件的基本使用
- [uni-read-pages](https://github.com/SilurianYang/uni-read-pages) ：自动读取 `pages.json` 所有配置。
- [uni-simple-router](https://hhyang.cn/v2/start/quickstart.html) ：在uni-app中使用vue-router的方式进行跳转路由，路由拦截。

### 定时任务

- [Python3](https://www.python.org/downloads/windows/) -熟悉 python3 基础语法
- [APScheduler](https://github.com/agronholm/apscheduler) - 熟悉定时任务框架
- [MongoDB](https://www.mongodb.com/) 和 [Redis](https://redis.io/)  - 熟悉数据存储数据库

## 安装和使用

获取代码

```
git clone https://gitee.com/ktianc/kinit.git
```

### 准备工作

```
Python == 3.10 (其他版本均未测试)
nodejs >= 14.0 (推荐使用最新稳定版)
Mysql >= 8.0
MongoDB (推荐使用最新稳定版)
Redis (推荐使用最新稳定版)
```

### 后端

1. 安装依赖

   ```
   cd kinit-api
   
   pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
   ```

2. 修改项目环境配置

   修改 `application/settings.py` 文件

   ```python
   # 安全警告: 不要在生产中打开调试运行!
   DEBUG = True # 如果当前为开发环境则改为 True，如果为生产环境则改为 False

3. 修改项目数据库配置信息

   在 `application/config` 目录中

   - development.py：开发环境

   - production.py：生产环境

   ```python
   # Mysql 数据库配置项
   # 连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
   # 数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
   
   SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称"
   SQLALCHEMY_DATABASE_TYPE = "mysql"
   
   
   # Redis 数据库配置
   REDIS_DB_ENABLE = True
   REDIS_DB_URL = "redis://:密码@地址:端口/数据库"
   
   # MongoDB 数据库配置
   MONGO_DB_ENABLE = True
   MONGO_DB_NAME = "数据库名称"
   MONGO_DB_URL = f"mongodb://用户名:密码@地址:端口/?authSource={MONGO_DB_NAME}"
   
   # 阿里云对象存储OSS配置
   # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
   # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，
   # Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
   #  *  [accessKeyId] {String}：通过阿里云控制台创建的AccessKey。
   #  *  [accessKeySecret] {String}：通过阿里云控制台创建的AccessSecret。
   #  *  [bucket] {String}：通过控制台或PutBucket创建的bucket。
   #  *  [endpoint] {String}：bucket所在的区域， 默认oss-cn-hangzhou。
   ALIYUN_OSS = {
       "accessKeyId": "accessKeyId",
       "accessKeySecret": "accessKeySecret",
       "endpoint": "endpoint",
       "bucket": "bucket",
       "baseUrl": "baseUrl"
   }
   
   # 获取IP地址归属地
   # 文档：https://user.ip138.com/ip/doc
   IP_PARSE_ENABLE = True
   IP_PARSE_TOKEN = "IP_PARSE_TOKEN"

4. 并在`alembic.ini`文件中配置数据库信息，用于数据库映射

   ```python
   # mysql+pymysql://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
   
   [dev]
   # 开发环境
   version_locations = %(here)s/alembic/versions_dev
   sqlalchemy.url = sqlalchemy.url = mysql+pymysql://root:123456@127.0.0.1/kinit
   
   
   [pro]
   # 生产环境
   version_locations = %(here)s/alembic/versions_pro
   sqlalchemy.url = sqlalchemy.url = mysql+pymysql://root:123456@127.0.0.1/kinit
   ```

5. 创建数据库

   ```
   mysql> create database kinit;             # 创建数据库
   mysql> use kinit;                         # 使用已创建的数据库 
   mysql> set names utf8;                    # 设置编码
   ```

6. 初始化数据库数据

   ```python
   # 项目根目录下执行，需提前创建好数据库
   # 会自动将模型迁移到数据库，并生成初始化数据
   # 执行前请确认执行的环境与settings.py文件中配置的DEBUG一致
   
   # （生产环境）
   python3 main.py init
   
   # （开发环境）
   python3 main.py init --env dev
   ```

7. 修改项目基本配置信息

   修改数据库表 - vadmin_system_settings 中的关键信息

   ```
   # 阿里云短信配置
   sms_access_key
   sms_access_key_secret
   sms_sign_name_1
   sms_template_code_1
   sms_sign_name_2
   sms_template_code_2
   
   # 高德地图配置
   map_key
   
   # 微信小程序配置
   wx_server_app_id
   wx_server_app_secret
   
   # 邮箱配置
   email_access
   email_password
   email_server
   email_port
   ```

8. 启动

   ```
   # 进入项目根目录下执行
   python3 main.py run
   ```

### PC端

1. 安装依赖

```
cd kinit-admin

pnpm install
```

2. 运行

```
pnpm run dev
```

3. 打包

```
pnpm run build:pro
```

### 定时任务

1. 安装依赖

   ```
   # 安装依赖库
   pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
   
   # 第三方源：
   1. 阿里源： https://mirrors.aliyun.com/pypi/simple/
   ```

2. 修改项目数据库配置信息

   在 `application/config` 目录中

   - development.py：开发环境

   - production.py：生产环境

   ```python
   # MongoDB 数据库配置
   # 与接口是同一个数据库
   MONGO_DB_NAME = "数据库名称"
   MONGO_DB_URL = f"mongodb://用户名:密码@地址:端口/?authSource={MONGO_DB_NAME}"
   
   
   # Redis 数据库配置
   # 与接口是同一个数据库
   REDIS_DB_URL = "redis://:密码@地址:端口/数据库名称"
   ```
   
3. 启动

   ```
   python3 main.py
   ```


### 访问项目

- 访问地址：http://localhost:5000 (默认为此地址，如有修改请按照配置文件)
- 账号：`15020221010` 密码：`kinit2022`
- 接口地址：http://localhost:9000/docs (默认为此地址，如有修改请按照配置文件)

## Docker Compose 生产环境部署

### 准备工作

1. 获取代码

   ```
   git clone https://gitee.com/ktianc/kinit.git
   ```

2. 修改项目环境配置：

   1. 修改 API 端：

      文件路径为：`kinit-api/application/settings.py`

      ```python
      # 安全警告: 不要在生产中打开调试运行!
      DEBUG = False # 生产环境应该改为 False
      ```

   2. 修改定时任务端：

      文件路径为：`kinit-task/application/settings.py`

      ```python
      # 安全警告: 不要在生产中打开调试运行!
      DEBUG = False # 生产环境应该改为 False
      ```

3. 如果已有 Mysql 或者 Redis 或者 MongoDB 数据库，请修改如下内容，如果没有则不需要修改：

   1. 修改 API 端配置文件：

      文件路径为：`kinit-api/application/config/production.py`

      ```python
      # Mysql 数据库配置项
      # 连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
      # 数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
      SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@177.8.0.7:3306/kinit"
      
      # Redis 数据库配置
      # 格式："redis://:密码@地址:端口/数据库名称"
      REDIS_DB_ENABLE = True
      REDIS_DB_URL = "redis://:123456@177.8.0.5:6379/1"
      
      # MongoDB 数据库配置
      # 格式：mongodb://用户名:密码@地址:端口/?authSource=数据库名称
      MONGO_DB_ENABLE = True
      MONGO_DB_NAME = "kinit"
      MONGO_DB_URL = f"mongodb://kinit:123456@177.8.0.6:27017/?authSource={MONGO_DB_NAME}"
      ```
      
   2. 修改定时任务配置文件
   
      文件路径为：`kinit-task/application/config/production.py`
   
      ```python
      # Redis 数据库配置
      # 与接口是同一个数据库
      # 格式："redis://:密码@地址:端口/数据库名称"
      REDIS_DB_ENABLE = True
      REDIS_DB_URL = "redis://:123456@177.8.0.5:6379/1"
      
      # MongoDB 数据库配置
      # 与接口是同一个数据库
      # 格式：mongodb://用户名:密码@地址:端口/?authSource=数据库名称
      MONGO_DB_ENABLE = True
      MONGO_DB_NAME = "kinit"
      MONGO_DB_URL = f"mongodb://kinit:123456@177.8.0.6:27017/?authSource={MONGO_DB_NAME}"
      ```
      
   3. 将已有的数据库在 `docker-compose.yml` 文件中注释
   
4. 配置阿里云 OSS 与 IP 解析接口地址（可选）

   文件路径：`kinit-api/application/config/production.py`

   ```python
   # 阿里云对象存储OSS配置
   # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
   # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，
   # Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
   #  *  [accessKeyId] {String}：通过阿里云控制台创建的AccessKey。
   #  *  [accessKeySecret] {String}：通过阿里云控制台创建的AccessSecret。
   #  *  [bucket] {String}：通过控制台或PutBucket创建的bucket。
   #  *  [endpoint] {String}：bucket所在的区域， 默认oss-cn-hangzhou。
   ALIYUN_OSS = {
       "accessKeyId": "accessKeyId",
       "accessKeySecret": "accessKeySecret",
       "endpoint": "endpoint",
       "bucket": "bucket",
       "baseUrl": "baseUrl"
   }
   
   # 获取IP地址归属地
   # 文档：https://user.ip138.com/ip/doc
   IP_PARSE_ENABLE = False
   IP_PARSE_TOKEN = "IP_PARSE_TOKEN"
   ```
   
5. 前端项目打包：

   ```shell
   cd kinit-admin
   
   # 安装依赖包
   pnpm install
   
   # 打包
   pnpm run build:pro
   ```

### 启动并初始化项目

```shell
# 启动并创建所有容器
docker-compose up -d

# 初始化数据
docker-compose exec kinit-api python3 main.py init

# 重启所有容器
docker-compose restart


# 其他命令：

# 停止所有容器
docker-compose down

# 查看所有容器状态
docker-compose ps -a
```

### 访问项目

- 访问地址：http://localhost (默认为此地址，如有修改请按照配置文件)
- 账号：`15020221010` 密码：`kinit2022`
- 接口地址：http://localhost:9000/docs (默认为此地址，如有修改请按照配置文件)

## 如何贡献

你可以[提一个 issue](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fkailong321200875%2Fvue-element-plus-admin%2Fissues%2Fnew) 或者提交一个 Pull Request。

**Pull Request:**

1. Fork 代码
2. 创建自己的分支: `git checkout -b feat/xxxx`
3. 提交你的修改: `git commit -am 'feat(function): add xxxxx'`
4. 推送您的分支: `git push origin feat/xxxx`
5. 提交 `pull request`

## 浏览器支持

本地开发推荐使用 `Chrome 80+` 浏览器

支持现代浏览器, 不支持 IE

| IE          | Edge            | Firefox         | Chrome          | Safari          |
| ----------- | --------------- | --------------- | --------------- | --------------- |
| not support | last 2 versions | last 2 versions | last 2 versions | last 2 versions |

## 许可证

[MIT](https://gitee.com/kailong110120130/vue-element-plus-admin/blob/master/LICENSE)

## PC端演示图

![image-20221010214526082](https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/1687232679892.jpg)

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373476/1695373476b028a6f9.jpg)

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373476/16953734768af98563.jpg)

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373476/169537347630c0e225.jpg)

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373476/1695373476da1a414f.jpg)

![1688392266702](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373475/1695373475fca1d7b8.jpg)

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373475/16953734756617d25d.jpg)

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373477/169537347735257fe5.jpg)

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373478/1695373478511f21e3.jpg)

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373477/16953734770decc360.jpg)

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695373477/169537347735257fe5.jpg)

![image-20221010214526082](https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/1687233000595-10.jpg)

## 另一种布局演示图

图1

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695375057/1695375057ebef7bd9.jpg)





图2

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695375057/1695375057abf3dcf6.jpg)





图3

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695375057/16953750571f2f9f7e.jpg)





图4

![image-20221010214526082](https://ktianc.oss-cn-beijing.aliyuncs.com/resource/images/1695375058/1695375058542fcf76.jpg)



## 微信小程序端演示图

<table>
    <tr>
        <td><img src="https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/1670077811740.jpg"/></td>
        <td><img src="https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/1670077826257.jpg"/></td>
		<td><img src="https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/1670077835024.jpg"/></td>
    </tr>
	<tr>
        <td><img src="https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/1670077849753.jpg"/></td>
        <td><img src="https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/1670077860987.jpg"/></td>
		<td><img src="https://k-typora.oss-cn-beijing.aliyuncs.com/kinit/1670077870240.jpg"/></td>
    </tr>
</table>