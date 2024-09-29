from __future__ import absolute_import, unicode_literals
# 이 파일에서 Celery 앱을 가져옴
from .celery import app as celery_app
__all__ = ('celery_app',)