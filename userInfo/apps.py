from django.apps import AppConfig


class UserinfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userInfo'

class ScholarshipsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name='scholarsips'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        from celery import current_app

        #Celery Beat Crontab Schedule 설정
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=40, #매 정시에 실행
            hour=20, #12시 정각(정오)
        )

        #Periodic Task 생성
        PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name='Send Deadline Email Task',
            task='userInfo.tasks.send_deadline_email',
        )