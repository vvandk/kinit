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

- 👭后端采用 Python 语言现代、快速（高性能） [FastAPI](https://fastapi.tiangolo.com/zh/) 异步框架 + [SQLAlchemy](https://www.sqlalchemy.org/) 异步操作 [MySQL](https://www.mysql.com/) 数据库。
- 🧑‍🤝‍🧑前端采用 [vue-element-plus-admin](https://gitee.com/kailong110120130/vue-element-plus-admin) 、[Vue3](https://cn.vuejs.org/guide/introduction.html)、[Element Plus](https://element-plus.gitee.io/zh-CN/guide/design.html)、[TypeScript](https://www.tslang.cn/)，等主流技术开发。
- 👫权限认证使用[（哈希）密码和 JWT Bearer 令牌的 OAuth2](https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/)，支持多终端认证系统。
- 👬支持加载动态权限菜单，多方式轻松权限控制，按钮级别权限控制。
- 👬已加入常见的`Redis`、`MYSQL`、`MongoDB`数据库异步操作。
- 开箱即用的中后台解决方案，可以用来作为新项目的启动模版，也可用于学习参考。并且时刻关注着最新技术动向，尽可能的第一时间更新。
- 与 [vue-element-plus-admin](https://gitee.com/kailong110120130/vue-element-plus-admin) 前端框架时刻保持同步更新。

## 特别鸣谢

[vue-element-plus-admin](https://gitee.com/kailong110120130/vue-element-plus-admin)：一套基于vue3、element-plus、typescript4、vite3的后台集成方案

[django-vue-admin](https://gitee.com/liqianglog/django-vue-admin)：基于RBAC模型的权限控制的一整套基础开发平台，前后端分离，后端采用 django+django-rest-framework，前端采用 vue+ElementUI。

[Ant Design Pro](https://preview.pro.ant.design/dashboard/analysis)：开箱即用的中台前端/设计解决方案

[Gin-Vue-Admin](https://demo.gin-vue-admin.com)：基于vite+vue3+gin搭建的开发基础平台（支持TS,JS混用），集成jwt鉴权，权限管理，动态路由，显隐可控组件，分页封装，多点登录拦截，资源权限，上传下载，代码生成器，表单生成器等开发必备功能。

[Vben Admin (vvbin.cn)](https://vvbin.cn/next)：Vue Vben Admin 是一个免费开源的中后台模版。使用了最新的`vue3`,`vite2`,`TypeScript`等主流技术开发，开箱即用的中后台前端解决方案，也可用于学习参考。

[中华人民共和国行政区划 (github.com)](https://github.com/modood/Administrative-divisions-of-China)：省级（省份）、 地级（城市）、 县级（区县）、 乡级（乡镇街道）、 村级（村委会居委会） ，中国省市区镇村二级三级四级五级联动地址数据。

[Vue Admin Plus](https://vue-admin-beautiful.com/admin-plus/#/index)：vue-admin-better是github开源admin中最优秀的集成框架之一，它是国内首个基于vue3.0的开源admin项目，同时支持电脑，手机，平板，默认分支使用vue3.x+antdv开发，master分支使用的是vue2.x+element开发。

[小诺开源技术 (xiaonuo.vip)](https://www.xiaonuo.vip/)：国内首个国密前后端分离快速开发平台

[my-web:](https://gitee.com/newgateway/my-web)：MyWeb 是一个企业级中后台前端/设计解决方案的的项目工程模板，它可以帮助你快速搭建企业级中后台产品原型

## 在线体验

演示地址：http://kinit.ktianc.top/

- 账号：15020221010
- 密码：kinit2022

## 源码地址

gitee地址(主推)：https://gitee.com/ktianc/kinit

github地址：https://github.com/vvandk/kinit

## 内置功能

- [x] 👨‍⚕️菜单管理：配置系统菜单，操作权限，按钮权限标识、后端接口权限等。

- [x] 👩‍⚕️角色管理：角色菜单权限分配。

- [x] 👨‍🎓用户管理：用户是系统操作者，该功能主要完成系统用户配置。

- [x] 🏡个人主页：配置用户个人信息，密码修改等。

- [x] 📚字典管理：对系统中经常使用的一些较为固定的数据进行维护。

- [x] 📁文件上传：对接阿里云OSS与本地存储。

- [x] 🔒登录认证：目前支持用户使用手机号+密码方式登录。

  说明：新建用户密码默认为手机号后六位；

  说明：用户在第一次登录时，必须修改当前用户密码。

- [x] 系统配置：对本系统环境信息进行动态配置

  网站标题，LOGO，描述，ICO，备案号，底部内容，百度统计代码，等等

- [x] 用户分布：接入高德地图显示各地区用户分布情况

- [x] 🗓️登录日志：用户登录日志记录和查询。

- [x] 🗓️操作日志：系统用户每次操作功能时的详细记录。

- [ ] **🗓️异常日志：获取并展示接口异常日志**

- [x] 🧾接口文档：提供自动生成的交互式 API 文档，与 ReDoc 文档

- [x] 导入导出：灵活支持数据导入导出功能

- [x] 手机验证码登录功能

- [x] 简单适配手机端：

  1. 工作台招呼语一行显示，多余显示省略号
  2. 查询框宽度统一，需手动调整（强迫症建议）
  3. 分页符更新，电脑端与手机端分页功能不同
  4. 表格工具栏更新，手机端取消文字显示
  5. 表格操作按钮多的时候自动叠起

- [x] 已加入常见的`Redis`、`MYSQL`、`MongoDB`数据库异步操作。

## TODO

- [ ] 考虑支持多机部署方案，如果接口使用多机，那么用户是否支持统一认证
- [ ] **自动化编排服务：使用docker-compose部署项目**
- [ ] **数据库备份：自动备份数据库**
- [ ] **接入数据大屏**
- [ ] **可视化低代码表单：接入低代码表单，https://vform666.com/vform3.html?from=element_plus**

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

### 依赖包

#### 前端

- [vue3-json-viewer](https://gitee.com/isfive/vue3-json-viewer)：简单易用的json内容展示组件,适配vue3和vite。
- [vue3-slide-verify](https://github.com/monoplasty/vue3-slide-verify)：滑块验证码插件 vue3 + typescript
- [SortableJS/vue.draggable.next](https://github.com/SortableJS/vue.draggable.next)：Vue 组件 （Vue.js 3.0） 允许拖放和与视图模型数组同步。
- [高德地图API (amap.com)](https://lbs.amap.com/api/jsapi-v2/guide/webcli/map-vue1)：地图 JSAPI 2.0 是高德开放平台免费提供的第四代 Web 地图渲染引擎， 以 WebGL 为主要绘图手段，本着“更轻、更快、更易用”的服务原则，广泛采用了各种前沿技术，交互体验、视觉体验大幅提升，同时提供了众多新增能力和特性。

#### 后端

- [iP查询接口文档](https://user.ip138.com/ip/doc)：IP查询第三方服务，有1000次的免费次数

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

3. 创建数据库

```shell
mysql> create database kinit;             # 创建数据库
mysql> use kinit;                         # 使用已创建的数据库 
mysql> set names utf8;                    # 设置编码
```

4. 映射数据库

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

5. 导入数据库数据

导入数据库数据前，请先保存映射后数据库中`alembic_version`表中的`version_num`数据

导入完成后，将此数据替换到导入后的对应字段

```shell
# 数据库文件地址：kinit-api/static/kinit.sql
# 导入命令
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

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/6.png)

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/5.png)

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/7.png)

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/8.png)

![image-20221010214526082](https://gitee.com/ktianc/kinit/raw/master/images/9.png)