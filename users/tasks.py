from django_redis import get_redis_connection
from django.core.mail import EmailMessage
from scholli.celery import app
from .utils import sendEmailHelper

@app.task
def send_email(email):
    code = sendEmailHelper.make_random_code()
    client.set(email, code, ex=300)  #email 키에 code 값을 300초(5분)동안 저장
    message = code
    subject = "%s" % "[SCHOLLI] 이메일 인증 코드 안내"
    to = [email]
    mail = EmailMessage(subject=subject, body=message, to=to)
    # mail.coontent_subtype="html"
    mail.send()
    return "Success to send email"
