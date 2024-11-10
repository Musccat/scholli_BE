from django.core.mail import EmailMessage
from wtnt.celery import app
from .utils import sendEmailHelper

@app.task
def send_email(email):
    code = sendEmailHelper.make_random_code()
    message = code
    subject = "%s" % "[SCHOLLI] 이메일 인증 코드 안내"
    to = [email]
    mail = EmailMessage(subject=subject, body=message, to=to)
    # mail.coontent_subtype="html"
    mail.send()
    return "Success to send email"
