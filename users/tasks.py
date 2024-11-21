from django_redis import get_redis_connection
from django.core.mail import EmailMessage
from scholli.celery import app
from .utils import sendEmailHelper

@app.task
def send_email(email, message):

    #이메일 설정
    subject = "%s" % "[SCHOLLI] 이메일 인증 코드 안내"
    mail = EmailMessage(subject=subject, body=message, to=[email])
    mail.coontent_subtype="html"
    mail.send()
    
    return "Success to send email"
