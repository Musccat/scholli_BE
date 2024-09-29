from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django의 settings 모듈을 Celery가 사용할 수 있도록 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholli.settings')

app = Celery('scholli')

# Django의 설정을 Celery에 적용
app.config_from_object('django.conf:settings', namespace='CELERY')

# 자동으로 tasks.py에서 task를 찾음
app.autodiscover_tasks()