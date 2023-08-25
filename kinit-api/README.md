# FastAPI 项目

fastapi Github：https://github.com/tiangolo/fastapi

fastapi 官方文档：https://fastapi.tiangolo.com/zh/

fastapi 更新说明：https://fastapi.tiangolo.com/zh/release-notes/

pydantic 官方文档：https://pydantic-docs.helpmanual.io/

pydantic 数据模型代码生成器官方文档 （Json -> Pydantic）：https://koxudaxi.github.io/datamodel-code-generator/

SQLAlchemy-Utils：https://sqlalchemy-utils.readthedocs.io/en/latest/

alembic 中文文档：https://hellowac.github.io/alembic_doc/zh/_front_matter.html

Typer 官方文档：https://typer.tiangolo.com/

SQLAlchemy 2.0 （官方）: https://docs.sqlalchemy.org/en/20/intro.html#installation

SQLAlchemy 1.4 迁移到 2.0 （官方）：https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#whatsnew-20-orm-declarative-typing

PEP 484 语法（官方）：https://peps.python.org/pep-0484/


## 项目结构

使用的是仿照 Django 项目结构：

- alembic：数据库迁移配置目录
  - versions_dev：开发环境数据库迁移文件目录
  - versions_pro：生产环境数据库迁移文件目录
  - env.py：映射类配置文件
- application：主项目配置目录，也存放了主路由文件
  - config：基础环境配置文件
    - development.py：开发环境
    - production.py：生产环境
  - settings.py：主项目配置文件
  - urls.py：主路由文件
- apps：项目的app存放目录
  - vadmin：基础服务
    - auth：用户 - 角色 - 菜单接口服务
      - models：ORM 模型目录
      - params：查询参数依赖项目录
      - schemas：pydantic 模型，用于数据库序列化操作目录
      - utils：登录认证功能接口服务
      - curd.py：数据库操作
      - views.py：视图函数
- core：核心文件目录
  - crud.py：关系型数据库操作核心封装
  - database.py：关系型数据库核心配置
  - data_types.py：自定义数据类型
  - exception.py：异常处理
  - logger：日志处理核心配置
  - middleware.py：中间件核心配置
  - dependencies.py：常用依赖项
  - event.py：全局事件
  - mongo_manage.py：mongodb 数据库操作核心封装
  - validator.py：pydantic 模型重用验证器
- db：ORM模型基类
- logs：日志目录
- static：静态资源存放目录
- utils：封装的一些工具类目录
- main.py：主程序入口文件
- alembic.ini：数据库迁移配置文件

## 开发环境

开发语言：Python 3.10

开发框架：Fastapi 0.101.1

ORM 框架：SQLAlchemy 2.0.20

## 开发工具

Pycharm 2022.3.2

推荐插件：Chinese (Simplified) Language Pack / 中文语言包

代码样式配置：

![image-20230315194534959](https://ktianc.oss-cn-beijing.aliyuncs.com/kinit/public/images/image-20230315194534959.png)

## 使用

```
source /opt/env/kinit-pro/bin/activate

# 安装依赖库
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 第三方源：

1. 阿里源： https://mirrors.aliyun.com/pypi/simple/

# 线上安装更新依赖库
/opt/env/kinit-pro-310/bin/pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 数据初始化

```shell
# 项目根目录下执行，需提前创建好数据库，并且数据库应该为空
# 会自动将模型迁移到数据库，并生成初始化数据

# 在执行前一定要确认要操作的环境与application/settings.DEBUG 设置的环境是一致的，
# 不然会导致创建表和生成数据不在一个数据库中！！！！！！！！！！！！！！！！！！！！！！

# 比如要初始化开发环境，那么env参数应该为 dev，并且 application/settings.DEBUG 应该 = True
# 比如要初始化生产环境，那么env参数应该为 pro，并且 application/settings.DEBUG 应该 = False

# 生产环境
python main.py init

# 开发环境
python main.py init --env dev
```

### 运行启动

```shell
# 直接运行main文件
python main.py run
```

## 其他操作

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

# 执行命令（开发环境）：
python main.py migrate --env dev

# 开发环境的原命令
alembic --name dev revision --autogenerate -m 2.0
alembic --name dev upgrade head
```

生成迁移文件后，会在alembic迁移目录中的version目录中多个迁移文件

## 查询数据

### 自定义的一些查询过滤

```python
# 日期查询
# 值的类型：str
# 值得格式：%Y-%m-%d：2023-05-14
字段名称=("date", 值)

# 模糊查询
# 值的类型: str
字段名称=("like", 值)

# in 查询
# 值的类型：list
字段名称=("in", 值)

# 时间区间查询
# 值的类型：tuple 或者 list
字段名称=("between", 值)

# 月份查询
# 值的类型：str
# 值的格式：%Y-%m：2023-05
字段名称=("month", 值)

# 不等于查询
字段名称=("!=", 值)

# 大于查询
字段名称=(">", 值)

# 等于 None
字段名称=("None")

# 不等于 None
字段名称=("not None")
```

代码部分：

```python
def __dict_filter(self, **kwargs) -> list[BinaryExpression]:
    """
    字典过滤
    :param model:
    :param kwargs:
    """
    conditions = []
    for field, value in kwargs.items():
        if value is not None and value != "":
            attr = getattr(self.model, field)
            if isinstance(value, tuple):
                if len(value) == 1:
                    if value[0] == "None":
                        conditions.append(attr.is_(None))
                    elif value[0] == "not None":
                        conditions.append(attr.isnot(None))
                    else:
                        raise CustomException("SQL查询语法错误")
                elif len(value) == 2 and value[1] not in [None, [], ""]:
                    if value[0] == "date":
                        # 根据日期查询， 关键函数是：func.time_format和func.date_format
                        conditions.append(func.date_format(attr, "%Y-%m-%d") == value[1])
                    elif value[0] == "like":
                        conditions.append(attr.like(f"%{value[1]}%"))
                    elif value[0] == "in":
                        conditions.append(attr.in_(value[1]))
                    elif value[0] == "between" and len(value[1]) == 2:
                        conditions.append(attr.between(value[1][0], value[1][1]))
                    elif value[0] == "month":
                        conditions.append(func.date_format(attr, "%Y-%m") == value[1])
                    elif value[0] == "!=":
                        conditions.append(attr != value[1])
                    elif value[0] == ">":
                        conditions.append(attr > value[1])
                    elif value[0] == "<=":
                        conditions.append(attr <= value[1])
                    else:
                        raise CustomException("SQL查询语法错误")
            else:
                conditions.append(attr == value)
    return conditions
```

示例：

查询所有用户id为1或2或 4或6，并且email不为空，并且名称包括李：

```python
users = UserDal(db).get_datas(limit=0, id=("in", [1,2,4,6]), email=("not None", ), name=("like", "李"))

# limit=0：表示返回所有结果数据
# 这里的 get_datas 默认返回的是 pydantic 模型数据
# 如果需要返回用户对象列表，使用如下语句：
users = UserDal(db).get_datas(
    limit=0,
    id=("in", [1,2,4,6]),
    email=("not None", ),
    name=("like", "李"),
    v_return_objs=True
)
```

查询所有用户id为1或2或 4或6，并且email不为空，并且名称包括李：

查询第一页，每页两条数据，并返回总数，同样可以通过 `get_datas` 实现原始查询方式：

```python
v_where = [VadminUser.id.in_([1,2,4,6]), VadminUser.email.isnot(None), VadminUser.name.like(f"%李%")]
users, count = UserDal(db).get_datas(limit=2, v_where=v_where, v_return_count=True)

# 这里的 get_datas 默认返回的是 pydantic 模型数据
# 如果需要返回用户对象列表，使用如下语句：
users, count = UserDal(db).get_datas(
    limit=2,
    v_where=v_where,
    v_return_count=True
    v_return_objs=True
)
```

### 外键查询示例

以常见问题表为主表，查询出创建用户名称为kinit的用户，创建了哪些常见问题，并加载出用户信息：

```python
v_options = [joinedload(VadminIssue.create_user)]
v_join = [["create_user"]]
v_where = [VadminUser.name == "kinit"]
datas = await crud.IssueCategoryDal(auth.db).get_datas(
    limit=0,
    v_options=options,
    v_join=v_join,
    v_where=v_where,
    v_return_objs=True
)
```

