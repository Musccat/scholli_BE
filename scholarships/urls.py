from django.urls import path
from .views import ScholarshipList, ScholarshipDetail, ScholarshipCreateView

urlpatterns = [
    path('', ScholarshipList.as_view(), name='scholarship-list'), # 장학금 목록
    path('register/', ScholarshipCreateView.as_view(), name='scholarship-register'),  # 장학금 등록
    path('<str:product_id>/', ScholarshipDetail.as_view(), name='scholarship-detail'),  # 장학금 상세
]
