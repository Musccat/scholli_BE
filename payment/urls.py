from django.urls import path
from .views import payment_page, PaymentView

urlpatterns = [
    path('page/', payment_page, name='payment_page'),  # 결제 페이지
    path('pay/', PaymentView.as_view(), name='pay'),  # 결제 정보 처리
]
