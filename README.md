# kinit

一天出租屋的下午，脑子里浮现出了多个画面，但是总是停留在了想，未行动，在娱乐。

这样的日子很不快乐，总想做点什么，但是总觉得做什么都很困难，不管了，我先做了再说。

因为热爱，所以拥抱未来！

## 介绍

kinit 是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。

- 🧑‍🤝‍🧑前端采用 [vue-element-plus-admin](https://gitee.com/kailong110120130/vue-element-plus-admin) 、[Vue3](https://cn.vuejs.org/guide/introduction.html)、[Element Plus](https://element-plus.gitee.io/zh-CN/guide/design.html)，[TypeScript](https://www.tslang.cn/)，等主流技术开发。
- 👭后端采用 Python 语言高性能 [FastAPI](https://fastapi.tiangolo.com/zh/) 框架以及强大的 Mysql 数据库。
- 👫权限认证使用[使用（哈希）密码和 JWT Bearer 令牌的 OAuth2](https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/)，支持多终端认证系统。
- 👬支持加载动态权限菜单，多方式轻松权限控制。
- 💏特别鸣谢：[django-vue-admin](https://gitee.com/liqianglog/django-vue-admin) 、 [vue-element-plus-admin](https://gitee.com/kailong110120130/vue-element-plus-admin)。
- 开箱即用的中后台解决方案，可以用来作为项目的启动模版，也可用于学习参考。并且时刻关注着最新技术动向，尽可能的第一时间更新。

## 在线体验

👩‍👧‍👦演示地址：[http://demo.django-vue-admin.com](https://gitee.com/link?target=http%3A%2F%2Fdemo.django-vue-admin.com)

- 账号：superadmin
- 密码：admin123456

## 源码地址

gitee地址(主推)：https://gitee.com/ktianc/kinit👩‍👦‍👦

github地址：https://gitee.com/ktianc/kinit👩‍👦‍👦

## 内置功能

- [x] 👨‍⚕️菜单管理：配置系统菜单，操作权限，按钮权限标识、后端接口权限等。
- [x] 👩‍⚕️角色管理：角色菜单权限分配。
- [x] 👨‍🎓用户管理：用户是系统操作者，该功能主要完成系统用户配置。
- [x] 🧑‍🔧字典管理：对系统中经常使用的一些较为固定的数据进行维护。
- [ ] 📁附件管理：对平台上所有文件、图片等进行统一管理。
- [ ] 🗓️登录日志：用户登录日志记录和查询。
- [ ] 🗓️操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。

##  前序准备

- [FastAPI](https://fastapi.tiangolo.com/zh/) - 熟悉后台接口 Web 框架
- [node](https://gitee.com/link?target=http%3A%2F%2Fnodejs.org%2F) 和 [git](https://gitee.com/link?target=https%3A%2F%2Fgit-scm.com%2F) - 项目开发环境
- [Vite](https://gitee.com/link?target=https%3A%2F%2Fvitejs.dev%2F) - 熟悉 vite 特性
- [Vue3](https://gitee.com/link?target=https%3A%2F%2Fv3.vuejs.org%2F) - 熟悉 Vue 基础语法
- [TypeScript](https://gitee.com/link?target=https%3A%2F%2Fwww.typescriptlang.org%2F) - 熟悉 `TypeScript` 基本语法
- [Es6+](https://gitee.com/link?target=http%3A%2F%2Fes6.ruanyifeng.com%2F) - 熟悉 es6 基本语法
- [Vue-Router-Next](https://gitee.com/link?target=https%3A%2F%2Fnext.router.vuejs.org%2F) - 熟悉 vue-router 基本使用
- [Element-Plus](https://gitee.com/link?target=https%3A%2F%2Felement-plus.org%2F) - element-plus 基本使用
- [Mock.js](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fnuysoft%2FMock) - mockjs 基本语法

## 安装和使用

获取代码

```
git clone https://gitee.com/ktianc/kinit.git
```

### 准备工作

```
Python >= 3.8.0 (推荐3.8+版本)
nodejs >= 14.0 (推荐最新)
Mysql >= 8.0
Redis(可选，最新版)
```

### 后端

1. 安装依赖

```
cd kinit-api

pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

2. 修改数据库信息

   在 `application/settings.py` 文件中配置数据库信息

   - mysql数据库版本建议：8.0
   - mysql数据库字符集：utf8mb4

```python
"""
数据库配置项
连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
"""
if DEBUG:
    # 测试库
    SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@127.0.0.1:3306/kinit"
    SQLALCHEMY_DATABASE_TYPE = "mysql"
else:
    # 正式库
    SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@127.0.0.1:3306/kinit"
    SQLALCHEMY_DATABASE_TYPE = "mysql"
```

3. 迁移数据库

```

```

4. 数据化数据库数据

```

```

5. 启动

```
python3 main.py
```

### 前端

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

### 访问项目

- 访问地址：http://localhost:5000 (默认为此地址，如有修改请按照配置文件)
- 账号：`superadmin` 密码：`admin123456`

## 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

## 浏览器支持

本地开发推荐使用 `Chrome 80+` 浏览器

支持现代浏览器, 不支持 IE

| IE          | Edge            | Firefox         | Chrome          | Safari          |
| ----------- | --------------- | --------------- | --------------- | --------------- |
| not support | last 2 versions | last 2 versions | last 2 versions | last 2 versions |

## 许可证

[MIT](https://gitee.com/kailong110120130/vue-element-plus-admin/blob/master/LICENSE)