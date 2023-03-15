# FastAPI 项目

fastapi 源代码：https://github.com/tiangolo/fastapi

fastapi 中文文档：https://fastapi.tiangolo.com/zh/

fastapi 更新说明：https://fastapi.tiangolo.com/zh/release-notes/

pydantic 官方文档：https://pydantic-docs.helpmanual.io/

pydantic 数据模型代码生成器官方文档 （Json -> Pydantic）：https://koxudaxi.github.io/datamodel-code-generator/

SQLAlchemy-Utils：https://sqlalchemy-utils.readthedocs.io/en/latest/

alembic 中文文档：https://hellowac.github.io/alembic_doc/zh/_front_matter.html

Typer 官方文档：https://typer.tiangolo.com/


## 项目结构

使用的是仿照 Django 项目结构：

- alembic：数据库迁移配置目录
- application：主项目配置目录，也存放了主路由文件
  - settings.py：主项目配置文件
  - urls.py：主路由文件
- apps：项目的app存放目录
- core：核心文件目录
  - database.py：关系型数据库核心配置
  - exception.py：异常处理
  - logger：日志处理核心配置
  - middleware.py：中间件核心配置
- db：ORM模型基类
- logs：日志目录
- static：静态资源存放目录
- tests：测试接口文件目录
- utils：封装的一些工具类目录
- main.py：主程序入口文件
- alembic.ini：数据库迁移配置文件

## 开发环境

开发语言：Python 3.10

开发框架：Fastapi 0.94.1

## 使用

```
source /opt/env/kinit-pro/bin/activate

# 安装依赖库
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 第三方源：

1. 阿里源： https://mirrors.aliyun.com/pypi/simple/
```

### 数据初始化

```shell
# 项目根目录下执行，需提前创建好数据库
# 会自动将模型迁移到数据库，并生成初始化数据
python main.py init
```

### 运行启动

```shell
# 直接运行main文件
python main.py run
```

## 其他

在线文档地址(在配置文件里面设置路径或者关闭)

```
http://127.0.0.1:9000/docs
```

Git更新ignore文件直接修改gitignore是不会生效的，需要先去掉已经托管的文件，修改完成之后再重新添加并提交。
```
第一步：
git rm -r --cached .
去掉已经托管的文件

第二步：
修改自己的igonre文件内容

第三步：
git add .
git commit -m "clear cached"
```

执行数据库迁移命令（终端执行）

```shell
# 执行命令（生产环境）：
python main.py migrate

# 执行命令（测试环境）：
python main.py migrate --env dev
```

生成迁移文件后，会在alembic迁移目录中的version目录中多个迁移文件