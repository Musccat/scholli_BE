from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import Wishlist
from scholarships.models import Scholarship


@shared_task
def send_deadline_email():
    #이틀 후 마감되는 장학금 조회
    two_days_from_now = now() + timedelta(days=2)
    scholarships = Scholarship.objects.filter(recruitment_end=two_days_from_now)

    for scholarship in scholarships :
        #해당 장학금을 위시리스트에 추가한 사용자 조회
        wishlists = Wishlist.objects.filter(scholarship=scholarship)

        for wishlist in wishlists:
            user = wishlist.user
            try:
                send_mail(
                    subject='[SCHOLLI] 장학금 신청 마감 안내',
                    message=f'{scholarship.name} 장학금의 신청 마감일이 {scholarship.recruitment_end}입니다. 서둘러 신청하세요!',
                    from_email=settings.DEFAULT_FROM_EMAIL,  # 발신자 이메일 (settings.py에 설정 필요)
                    recipient_list=[user.email],  # 수신자 이메일
                )
            except Exception as e:
                print(f"Error sending email to {user.email}: {e}")