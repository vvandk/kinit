

# kinit-task

**感谢若依：http://demo.ruoyi.vip/**



定时任务功能：

- [x] 支持添加四种定时任务：
  - [x] 添加 date 指定日期时间执行定时任务
  - [x] 添加 Cron 表达式定时任务
  - [x] 添加 Interval 时间间隔定时任务
  - [x] 支持立即执行任务功能
- [x] 使用 redis 消息队列功能动态添加任务
- [x] 使用 mongodb 数据库存储持久化保存任务
- [x] 任务表达式使用类路径表示，支持添加初始化参数：支持字符串，布尔类型，长整型，浮点型，整型

- [x] 每次任务执行完成后，记录日志到 mongodb 数据中：开始/结束执行时间，耗时，任务返回值，异常信息



## 使用

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
   """
   MongoDB 数据库配置
   
   与接口是同一个数据库
   """
   MONGO_DB_NAME = "数据库名称"
   MONGO_DB_URL = f"mongodb://用户名:密码@地址:端口/?authSource={MONGO_DB_NAME}"
   
   
   """
   Redis 数据库配置
   
   与接口是同一个数据库
   """
   REDIS_DB_URL = "redis://:密码@地址:端口/数据库名称"
   ```

3. 启动

   ```
   python3 main.py
   ```

   

## APScheduler

官方文档：https://apscheduler.readthedocs.io/en/master/userguide.html

Github：https://github.com/agronholm/apscheduler

PYPI：https://pypi.org/project/APScheduler/



安装/更新

```
pip install -U APScheduler -i https://mirrors.aliyun.com/pypi/simple/
```



### 使用

```
# 添加任务

from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    print('Hello world!')

scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', minutes=1)
scheduler.start()
```

```
# 立即执行

from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print("Hello, world!")

scheduler = BackgroundScheduler()

# 立即执行任务
scheduler.add_job(job, next_run_time=datetime.now(), id='my_job')

scheduler.start()
```

```
# 判断是否存在

from apscheduler.schedulers.background import BackgroundScheduler

def my_job():
    print('Hello, world!')

scheduler = BackgroundScheduler()
scheduler.add_job(my_job, 'interval', seconds=10, id='my_job')
scheduler.start()

# 检查任务是否存在
if scheduler.get_job('my_job'):
    print('任务存在')
else:
    print('任务不存在')
```

```
# 删除任务

from apscheduler.schedulers.background import BackgroundScheduler

def my_job():
    print('Hello, world!')

scheduler = BackgroundScheduler()
scheduler.add_job(my_job, 'interval', seconds=10, id='my_job')
scheduler.start()

# 删除任务
scheduler.remove_job('my_job')
```

```
# 添加参数

from apscheduler.schedulers.background import BackgroundScheduler

def job(arg1, arg2):
    print('This is a job with arguments: {}, {}'.format(arg1, arg2))

scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=5, args=('hello', 'world'))
scheduler.start()
```

```
# 获取当前正在执行的任务列表

from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print('This is a job.')

scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=5)
scheduler.start()

# 获取当前正在执行的任务列表
jobs = scheduler.get_jobs()
for job in jobs:
    print(job)
```

### 添加定时任务 add_job 方法

APScheduler的`add_job`方法用于添加定时任务。除了使用Cron表达式来指定定时任务的调度规则之外，`add_job`方法还支持其他几种方法来设置定时任务的执行时间。以下是`add_job`方法常用的几种调度方式：

- date：指定一个具体的日期和时间来执行任务。

```python
scheduler.add_job(job_function, 'date', run_date='2023-06-30 12:00:00')
```

在上述示例中，任务将在指定的日期和时间（2023年6月30日12:00:00）执行。

- interval：指定一个时间间隔来执行任务。

```python
scheduler.add_job(job_function, 'interval', minutes=30)
```

在上述示例中，任务将每隔30分钟执行一次。

- cron：使用Cron表达式来指定任务的执行时间。

```python
scheduler.add_job(job_function, 'cron', hour=8, minute=0, day_of_week='0-4')
```

在上述示例中，任务将在每个工作日的早上8点执行。

- timedelta：指定一个时间间隔来执行任务，但相对于当前时间的偏移量。

```python
from datetime import timedelta

scheduler.add_job(job_function, 'interval', seconds=10, start_date=datetime.now() + timedelta(seconds=5))
```

在上述示例中，任务将在当前时间的5秒后开始执行，然后每隔10秒执行一次。

这些方法提供了不同的方式来安排定时任务的执行时间。你可以根据具体需求选择适合的调度方式，并结合相关参数来设置定时任务的执行规则。无论使用哪种方法，都可以通过`add_job`方法将任务添加到调度器中，以便按照预定的时间规则执行任务。

### cron 触发器

`cron`触发器是`APScheduler`中常用的一种触发器类型，用于基于cron表达式来触发任务。它提供了灵活且精确的任务调度规则，可以在特定的日期和时间点上触发任务。

以下是关于`cron`触发器的详细解释：

1. **创建触发器：**要创建一个`cron`触发器，可以使用`CronTrigger`类并指定cron表达式作为参数。cron表达式是一种字符串格式，用于指定任务触发的时间规则。它由多个字段组成，每个字段表示时间的不同部分，例如分钟、小时、日期等。示例代码如下：

   ```python
   from apscheduler.triggers.cron import CronTrigger
   
   # 创建每天上午10点触发的cron触发器
   trigger = CronTrigger(hour=10)
   ```

   在上述示例中，我们创建了一个每天上午10点触发的`cron`触发器。

2. **添加触发器到任务：**创建触发器后，可以将它与任务相关联，以定义任务的调度规则。可以使用`add_job()`方法的`trigger`参数将触发器添加到任务中。示例代码如下：

   ```python
   from apscheduler.schedulers.blocking import BlockingScheduler
   
   def job_function():
       # 任务逻辑
   
   scheduler = BlockingScheduler()
   scheduler.add_job(job_function, trigger=CronTrigger(hour=10))
   ```

   在上述示例中，我们将`cron`触发器添加到了名为`job_function`的任务中，使得该任务在每天上午10点触发。

3. **cron表达式：**cron表达式由多个字段组成，用空格分隔。每个字段表示时间的不同部分，具体如下：

   - `分钟`：范围是0-59。
   - `小时`：范围是0-23。
   - `日期`：范围是1-31。
   - `月份`：范围是1-12。
   - `星期几`：范围是0-6，其中0表示星期日，1表示星期一，以此类推。

   通过在cron表达式中指定相应的字段值，可以创建各种复杂的调度规则。例如：`0 12 * * *`表示每天中午12点触发，`0 8-18 * * MON-FRI`表示工作日每小时从早上8点到下午6点之间的整点触发。

   ```python
   from apscheduler.triggers.cron import CronTrigger
   
   # 创建每周一至周五上午10点触发的cron触发器
   trigger = CronTrigger(hour=10, day_of_week='mon-fri')
   ```

   在上述示例中，我们创建了一个每周一至周五上午10点触发的`cron`触发

### interval 触发器

`interval`触发器是`APScheduler`中常用的一种触发器类型，用于在固定的时间间隔内重复触发任务。它基于时间间隔而不是具体的日期和时间来触发任务，适用于需要以固定间隔执行的周期性任务。

以下是关于`interval`触发器的详细解释：

1. **创建触发器：**要创建一个`interval`触发器，可以使用`IntervalTrigger`类并指定时间间隔参数。时间间隔可以以秒、分钟、小时或者天为单位进行设置。示例代码如下：

   ```python
   from apscheduler.triggers.interval import IntervalTrigger
   
   # 创建每5秒触发一次的interval触发器
   trigger = IntervalTrigger(seconds=5)
   ```

   在上述示例中，我们创建了一个每5秒触发一次的`interval`触发器。

2. **添加触发器到任务：**创建触发器后，可以将它与任务相关联，以定义任务的调度规则。可以使用`add_job()`方法的`trigger`参数将触发器添加到任务中。示例代码如下：

   ```python
   from apscheduler.schedulers.blocking import BlockingScheduler
   
   def job_function():
       # 任务逻辑
   
   scheduler = BlockingScheduler()
   scheduler.add_job(job_function, trigger=IntervalTrigger(seconds=5))
   ```

   在上述示例中，我们将`interval`触发器添加到了名为`job_function`的任务中，使得该任务每隔5秒触发一次。

3. **触发器选项：**`IntervalTrigger`类还提供了其他可选的参数，用于进一步定制触发器的行为，例如：

   - `start_date`：指定触发器的开始日期和时间。
   - `end_date`：指定触发器的结束日期和时间。
   - `timezone`：指定触发器的时区。

   这些选项可以通过在创建触发器时传递相应的参数来设置。

   ```python
   from apscheduler.triggers.interval import IntervalTrigger
   from datetime import datetime, timedelta
   from pytz import timezone
   
   # 创建每5分钟触发一次的interval触发器，从指定日期开始，结束日期为一周后
   start_date = datetime(2023, 1, 1, 0, 0, 0)
   end_date = start_date + timedelta(weeks=1)
   tz = timezone('US/Eastern')
   trigger = IntervalTrigger(minutes=5, start_date=start_date, end_date=end_date, timezone=tz)
   ```

   在上述示例中，我们创建了一个每5分钟触发一次的`interval`触发器，并指定了开始日期、结束日期和时区。

通过使用`interval`触发器，可以方便地设置任务以固定的时间间隔重复执行。可以根据实际需求设置触发器的参数，以满足不同的周期性任务调度要求。

### 事件监听器

事件监听器是`APScheduler`中的一种机制，用于监视和响应调度器中的事件。当特定事件发生时，监听器将执行预定义的操作，例如记录日志、发送通知或执行自定义逻辑。下面是关于`APScheduler`事件监听器的详细解释：

1. **事件类型：**`APScheduler`中有多个事件类型，每个事件类型对应着不同的调度器行为或状态变化。一些常见的事件类型包括：
   - `EVENT_JOB_ADDED`：当添加新任务时触发。
   - `EVENT_JOB_REMOVED`：当移除任务时触发。
   - `EVENT_JOB_MODIFIED`：当修改任务时触发。
   - `EVENT_JOB_EXECUTED`：当任务执行完成时触发。
   - `EVENT_JOB_ERROR`：当任务执行出错时触发。
   - `EVENT_SCHEDULER_STARTED`：当调度器启动时触发。
   - `EVENT_SCHEDULER_SHUTDOWN`：当调度器关闭时触发。

### max_instances 最大实例

报错：

```
Execution of job "Test.main (trigger: interval[0:00:01], next run at: 2023-06-21 16:23:23 CST)" skipped: maximum number of running instances reached (1)
```

这个错误提示表示当前正在运行的任务实例数量已达到最大限制，因此调度器跳过了该任务的执行。该错误通常是由于设置了并发执行任务的限制导致的。

默认情况下，`APScheduler`允许同时运行的任务实例数量是1，也就是说同一任务在执行时不会与自身的其他实例并发执行。这是为了防止任务并发执行引发的问题，例如资源冲突或意外的行为。

如果你想要允许任务并发执行，可以通过调整调度器的配置来增加最大并发实例数量。在创建调度器时，可以传递`max_instances`参数来设置最大并发实例数量。示例如下：

```python
from apscheduler.schedulers.blocking import BlockingScheduler

def job_function():
    # 任务逻辑

scheduler = BlockingScheduler()
scheduler.add_job(job_function, 'interval', seconds=1, max_instances=5)  # 设置最大并发实例为5
scheduler.start()
```

在上述示例中，`max_instances`参数被设置为5，表示同一任务可以最多同时运行5个实例。如果同时触发了多个任务实例，调度器将会并发执行它们，直到达到最大实例数量为止。

请注意，增加最大并发实例数量可能会增加系统负载和资源消耗。因此，在设置并发执行之前，请确保你的系统能够处理额外的负载，并根据实际需求进行适当的配置。

### 如何达到了最大实例，那么超过最大实例的其他任务会延后执行吗

当调度器的任务实例数量达到最大限制时，超过最大实例数量的其他任务将会被延后执行。`APScheduler`会自动管理任务的执行队列，并按照任务的调度规则和最大实例限制进行调度。

具体来说，当有新的任务触发时，调度器会检查当前正在运行的任务实例数量是否已经达到最大限制。如果是，则该任务的执行会被延后，直到有可用的执行实例。延后执行的任务会继续保持在调度器的执行队列中，等待下一个可用的执行时机。

值得注意的是，任务的延后执行是相对于其原定的调度时间而言的。也就是说，即使一个任务被延后执行，它仍然会尽可能地在其下一个调度时间点之前执行，以保持任务的调度准确性。

以下是一个示例，演示了当任务实例数量达到最大限制时，其他任务会被延后执行：

```python
from apscheduler.schedulers.blocking import BlockingScheduler

def job_function():
    # 任务逻辑

scheduler = BlockingScheduler()
scheduler.add_job(job_function, 'interval', seconds=10, max_instances=2)  # 设置最大并发实例为2

# 添加多个任务，超过最大实例数量
for i in range(5):
    scheduler.add_job(job_function, 'interval', seconds=5)

scheduler.start()
```

在上述示例中，我们设置了最大并发实例数量为2，然后添加了5个间隔为5秒的任务。由于最大实例数量限制为2，所以前两个任务会立即开始执行，而后面的三个任务会被延后执行，等待前面的任务完成并释放实例后才能执行。

总结起来，超过最大实例数量的任务会被放入调度器的执行队列中，并在合适的时机进行延后执行，以保证任务的调度准确性和最大实例限制的有效性。

## Redis

### 什么是Redis消息订阅与发布

Redis是一个开源的高性能内存数据库，支持数据结构丰富、灵活的持久化、复制以及分片。而Redis消息订阅与发布就是Redis中的一种发布/订阅模型，调用方可以订阅某个频道并接收消息，也可以向某个频道发送消息，同时所有订阅该频道的调用方都可以收到这个消息。该模型使用了发布/订阅的方式来实现多个调用方之间的信息通信。

### Redis消息保留策略

Redis提供了两种消息保留策略，分别是无保留和有保留。无保留是指当发送者向某个频道发送消息时，如果没有订阅该频道的调用方，就直接将该消息丢弃。而有保留则是指Redis能够将消息保存下来，直到有订阅该频道的调用方出现时再将该消息发送给该调用方。在Redis中，消息保留策略由两个参数来控制，即PUBLISH命令的NX、EX和PX选项。NX选项表示只有当至少有一个订阅者收到消息时，该消息才会被保留。EX和PX选项用于控制保留策略的时间，EX表示以秒为单位的保留时间，PX表示以毫秒为单位的保留时间。开发者可以根据实际需要配置相应的保留策略。