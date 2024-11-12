from django_redis import get_redis_connection
from django.core.mail import EmailMessage
from scholli.celery import app
from .utils import sendEmailHelper

@app.task
def send_email(email):
    # Redis 연결 설정
    client = get_redis_connection("default") 
    code = sendEmailHelper.make_random_code()
    client.set(email, code, ex=300)  #email 키에 code 값을 300초(5분)동안 저장
    print("Saved in Redis:", client.get(email))
    client.set("test_email_code", code, ex=300)  # 고정된 키 이름으로 저장
    print("Saved in Redis:", client.get("test_email_code"))  # Redis에 저장된 값 확인
    message = code
    subject = "%s" % "[SCHOLLI] 이메일 인증 코드 안내"
    to = [email]
    mail = EmailMessage(subject=subject, body=message, to=to)
    # mail.coontent_subtype="html"
    mail.send()
    return "Success to send email"
