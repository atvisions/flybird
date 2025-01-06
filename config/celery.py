import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# 设置默认Django settings模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 创建Celery应用
app = Celery('flybird')

# 使用Django的settings文件配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 设置时区
app.conf.timezone = 'Asia/Shanghai'
app.conf.enable_utc = False

# 自动发现任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 定时任务配置
app.conf.beat_schedule = settings.CELERY_BEAT_SCHEDULE 