#!/bin/bash

# 启动 Celery Worker
celery -A config worker -l INFO &

# 启动 Celery Beat
celery -A config beat -l INFO &

# 等待所有后台进程完成
wait 