from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import Wishlist
from scholarships.models import Scholarship
from userInfo.models import UserSubscription
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_deadline_email():
    two_days_from_now = now() + timedelta(days=2)
    scholarships = Scholarship.objects.filter(recruitment_end=two_days_from_now)

    for scholarship in scholarships:
        #해당 장학금을 위시리스트에 추가한 사용자 조회
        wishlists = Wishlist.objects.filter(scholarship=scholarship)

        for wishlist in wishlists:
            user = wishlist.user
            try:
                # 사용자 구독 상태 확인
                subscription = UserSubscription.objects.get(user=user)
                if subscription.is_active:  # 구독이 활성화된 경우
                    # 템플릿 렌더링
                    email_context = {
                        'name': scholarship.name,
                        'documents': scholarship.required_documents_details,
                    }

                    email_html = render_to_string('email_template.html', email_context)

                    email=EmailMultiAlternatives(
                        subject='[SCHOLLI] 장학금 신청 마감 안내',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    email.attach_alternative(email_html, "text/html")  # HTML 버전 첨부
                    email.send()  # 이메일 발송
                    
            except UserSubscription.DoesNotExist: # 구독 정보가 없는 경우 무시
                continue
            except Exception as e:
                # 발송 실패 시 로깅
                print(f"Error sending email: {e}")

            
                
