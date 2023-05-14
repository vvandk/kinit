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

开发框架：Fastapi 0.95.0

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

# 执行命令（测试环境）：
python main.py migrate --env dev
```

生成迁移文件后，会在alembic迁移目录中的version目录中多个迁移文件

## 查询数据

### 查询过滤

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

![image-20230514113859232](D:\programming\ktianc\project\kinit-pro\images\image-20230514113859232.png)

示例：

查询所有用户id为1或2或 4或6，并且email不为空，并且名称包括李：

```python
users = UserDal(db).get_datas(limit=0, id=("in", [1,2,4,6]), email=("not None"), name=("like", "李"))
```

### v_join_query

外键字段查询，内连接

以常见问题类别表为例：

首先需要在 `crud.py/IssueCategoryDal` 的 `__init__` 方法中定义 `key_models`：

```python
class IssueCategoryDal(DalBase):

    def __init__(self, db: AsyncSession):
        key_models = {
            # 外键字段名，也可以自定义
            "create_user": {
                # 外键对应的orm模型
                "model": vadminAuthModels.VadminUser,
                # 如果对同一个模型只有一个外键关联时，下面这个 onclause 可以省略不写，一个以上时必须写，需要分清楚要查询的是哪个
                # 这里其实可以省略不写，但是为了演示这里写出来了
                "onclause": models.VadminIssueCategory.create_user_id == vadminAuthModels.VadminUser.id
            }
        }
        super(IssueCategoryDal, self).__init__(
            db,
            models.VadminIssueCategory,
            schemas.IssueCategorySimpleOut,
            key_models
        )
```

使用案例：

```python
async def test(self):
    """
    v_join_query 示例方法
    获取用户名称包含李 创建出的常见问题类别
    """
    v_join_query = {
        # 与 key_models 中定义的外键字段名定义的一样
        "create_user": {
            # 外键表字段名：查询值
            "name": ("like", "李")
        }
    }
    v_options = [joinedload(self.model.create_user)]
    datas = self.get_datas(limit=0, v_join_query=v_join_query, v_options=v_options)
```

完整案例：

```python
class IssueCategoryDal(DalBase):

    def __init__(self, db: AsyncSession):
        key_models = {
            # 外键字段名，也可以自定义
            "create_user": {
                # 外键对应的orm模型
                "model": vadminAuthModels.VadminUser,
                # 如果对同一个模型只有一个外键关联时，下面这个 onclause 可以省略不写，一个以上时必须写，需要分清楚要查询的是哪个
                # 这里其实可以省略不写，但是为了演示这里写出来了
                "onclause": models.VadminIssueCategory.create_user_id == vadminAuthModels.VadminUser.id
            }
        }
        super(IssueCategoryDal, self).__init__(
            db,
            models.VadminIssueCategory,
            schemas.IssueCategorySimpleOut,
            key_models
        )

    async def test(self):
        """
        v_join_query 示例方法
        获取用户名称包含李 创建出的常见问题类别
        """
        v_join_query = {
            # 与 key_models 中定义的外键字段名定义的一样
            "create_user": {
                # 外键表字段名：查询值
                "name": ("like", "李")
            }
        }
        v_options = [joinedload(self.model.create_user)]
        datas = self.get_datas(limit=0, v_join_query=v_join_query, v_options=v_options)
```

### v_or

或逻辑运算查询

语法：

```python
# 普通查询
v_or = [(字段名称, 值), (字段名称, 值), ... ]

# 模糊查询
v_or = [(字段名称, ("like", 值)), (字段名称, ("like", 值)), ... ]

# 组合查询
v_or = [(字段名称, ("like", 值)), (字段名称, ("in", [值, 值, 值, ...])), ... ]

# 外键查询，需要先定义 key_models
v_or = [("fk", key_models 中定义的外键字段名, 外键表字段名称, ("like", 值)), ("fk", key_models 中定义的外键字段名, 外键表字段名称, ("like", 值)), ... ]
```

比如查询一个用户手机号为`13409090909`或者`15390909090`：

```python
v_or = [("telephone", "13409090909"), ("telephone", "15390909090") ]
user = UserDal(db).get_data(v_or=v_or)
```

