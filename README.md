<div align="center">
    <p align="center">
        <img src="https://gitee.com/ktianc/kinit/raw/master/kinit-admin/public/logo.png" height="150" alt="logo"/>
    </p>
</div>



## [关于]

<div align="center"><h3 align="center">Kinit 是一套开箱即用的中后台解决方案，可以作为新项目的启动模版。</h3></div>
<div align="center"><h3 align="center">前后端分离架构，开箱即用，紧随前沿技术</h3></div>

<div align="center"><h3 align="center">因为热爱，所以拥抱未来！</h3></div>

## 介绍

Kinit 是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。

- 🧑‍🤝‍🧑前端采用 [vue-element-plus-admin](https://gitee.com/kailong110120130/vue-element-plus-admin) 、[Vue3](https://cn.vuejs.org/guide/introduction.html)、[Element Plus](https://element-plus.gitee.io/zh-CN/guide/design.html)、[TypeScript](https://www.tslang.cn/)，等主流技术开发。
- 👭后端采用 Python 语言高性能 [FastAPI](https://fastapi.tiangolo.com/zh/) 框架以及强大的 Mysql 数据库。
- 👫权限认证使用[（哈希）密码和 JWT Bearer 令牌的 OAuth2](https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/)，支持多终端认证系统。
- 👬支持加载动态权限菜单，多方式轻松权限控制。
- 💏特别鸣谢：[django-vue-admin](https://gitee.com/liqianglog/django-vue-admin) 、 [vue-element-plus-admin](https://gitee.com/kailong110120130/vue-element-plus-admin)。
- 开箱即用的中后台解决方案，可以用来作为新项目的启动模版，也可用于学习参考。并且时刻关注着最新技术动向，尽可能的第一时间更新。

## 在线体验

👩‍👧‍👦演示地址：http://kinit.ktianc.top/

- 账号：admin
- 密码：123456

## 源码地址

gitee地址(主推)：https://gitee.com/ktianc/kinit👩‍👦‍👦

github地址：https://gitee.com/ktianc/kinit👩‍👦‍👦

## 内置功能

- [x] 👨‍⚕️菜单管理：配置系统菜单，操作权限，按钮权限标识、后端接口权限等。

- [x] 👩‍⚕️角色管理：角色菜单权限分配。

- [x] 👨‍🎓用户管理：用户是系统操作者，该功能主要完成系统用户配置。

- [x] 🏡个人主页：配置用户个人信息，密码修改等。

- [x] 📚字典管理：对系统中经常使用的一些较为固定的数据进行维护。

- [ ] 📁附件管理：对平台上所有文件、图片等进行统一管理。

- [ ] 🗓️登录日志：用户登录日志记录和查询。

- [ ] 🗓️操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。

- [x] 🔒登录认证：目前支持用户使用手机号+密码方式登录。

  说明：新建用户密码默认为手机号后六位；

  说明：用户在第一次登录时，必须修改当前用户密码。

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
```

### 后端

1. 安装依赖

```
cd kinit-api

pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

2. 修改数据库信息

   在 `application/settings.py` 文件中配置数据库信息，用于项目连接

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
   
   并在`alembic.ini`文件中配置数据库信息，用于数据库映射
   
   ```python
   # mysql+pymysql://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
   sqlalchemy.url = mysql+pymysql://root:123456@127.0.0.1/kinit
   ```

3. 映射数据库

```shell
# 初次生成映射文件
alembic revision -m "生成映射文件"

# 通过该命令可以将模型映射到数据库
alembic upgrade head

# 如果有更新，则可以使用这个命令再次生成映射文件，初次也可以使用
alembic revision --autogenerate -m "update"
# --autogenerate：自动将当前模型的修改，生成映射脚本。

# 通过该命令可以将模型映射到数据库
alembic upgrade head
```

4. 导入数据库数据

   导入数据库数据前，请先保存映射后数据库中`alembic_version`表中的`version_num`数据

   导入完成后，将此数据替换到导入后的对应字段

```shell
# 数据库文件地址：kinit-api/static/kinit.sql
# 导入命令
mysql> create database kinit;             # 创建数据库
mysql> use kinit;                         # 使用已创建的数据库 
mysql> set names utf8;                    # 设置编码
mysql> source kinit-api/static/kinit.sql  # 导入备份数据库
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

## Git 贡献提交规范

- `feat` 新功能
- `fix` 修补 bug
- `docs` 文档
- `style` 格式、样式(不影响代码运行的变动)
- `refactor` 重构(即不是新增功能，也不是修改 BUG 的代码)
- `perf` 优化相关，比如提升性能、体验
- `test` 添加测试
- `build` 编译相关的修改，对项目构建或者依赖的改动
- `ci` 持续集成修改
- `chore` 构建过程或辅助工具的变动
- `revert` 回滚到上一个版本
- `workflow` 工作流改进
- `mod` 不确定分类的修改
- `wip` 开发中
- `types` 类型

## 浏览器支持

本地开发推荐使用 `Chrome 80+` 浏览器

支持现代浏览器, 不支持 IE

| IE          | Edge            | Firefox         | Chrome          | Safari          |
| ----------- | --------------- | --------------- | --------------- | --------------- |
| not support | last 2 versions | last 2 versions | last 2 versions | last 2 versions |

## 许可证

[MIT](https://gitee.com/kailong110120130/vue-element-plus-admin/blob/master/LICENSE)

## 演示图

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/1.png)

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/2.png)

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/3.png)

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/4.png)

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/5.png)