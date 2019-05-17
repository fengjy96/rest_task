from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_xops.settings')

app = Celery('rest_xops')

app.config_from_object('django.conf:settings')

# 自动发现 task，这个配置会自动从每个 app 目录下去发现 tasks.py 文件
app.autodiscover_tasks()

## 以下内容也可以写在 settings.py 文件中

# Broker 配置，使用 Redis 作为消息中间件
BROKER_URL = 'redis://localhost:6379/1'

# Backend 设置，使用 Redis 作为后端结果存储
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_ENABLE_UTC = False

# 防止任务死锁
CELERYD_FORCE_EXECV = True

# 并发的 worker 数量
CELERYD_CONCURRENCY = 8

CELERY_ACKS_LATE = True

# 每个 worker 最多执行的任务数
CELERYD_MAX_TASKS_PER_CHILD = 100

# 任务超时时间
CELERYD_TASK_TIME_LIMIT = 15 * 60
