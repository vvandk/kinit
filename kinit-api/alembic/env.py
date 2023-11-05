from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
import sys

from core.database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# 添加当前项目路径到环境变量
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 导入项目中的基本映射类，与 需要迁移的 ORM 模型
from apps.vadmin.auth.models import *
from apps.vadmin.system.models import *
from apps.vadmin.record.models import *
from apps.vadmin.help.models import *
from apps.vadmin.resource.models import *

# 修改配置中的参数
target_metadata = Base.metadata


def run_migrations_offline():
    """
    以“脱机”模式运行迁移。
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # 是否检查字段类型，字段长度
        compare_server_default=True  # 是否比较在数据库中的默认值
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    以“在线”模式运行迁移。
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # 是否检查字段类型，字段长度
            compare_server_default=True  # 是否比较在数据库中的默认值
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("offline")
    run_migrations_offline()
else:
    print("online")
    run_migrations_online()
