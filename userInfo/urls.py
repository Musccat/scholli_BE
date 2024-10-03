from django.urls import path
from .views import (ProfileCreateView, ProfileUpdateView, 
                    WishlistCreateView, WishlistDeleteView, WishlistListView, 
                    RecommendScholarshipsView, RecommendScholarshipsDetail, RecommendScholarListView)

urlpatterns = [
    path('profile/create/', ProfileCreateView.as_view(), name='profile-create'),  # 프로필 생성
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),  # 프로필 수정 (로그인된 사용자)
    path('wishlist/add/', WishlistCreateView.as_view(), name='wishlist-add'),  # 찜 추가
    path('wishlist/delete/<str:scholarship_id>/', WishlistDeleteView.as_view(), name='wishlist-delete'),  # 찜 삭제
    path('wishlist/', WishlistListView.as_view(), name='wishlist-list'),  # 찜 목록 조회
    path('scholarships/recommend/', RecommendScholarshipsView.as_view(), name='scholarship-recommend'), # 추천 장학금
    path('scholarships/recommend/list/', RecommendScholarListView.as_view(), name='scholarship-recommend-list'), # 추천 장학금 목록 
    path('scholarships/recommend/list/<str:product_id>/', RecommendScholarshipsDetail.as_view(), name='scholarship-recommend-detail'),  # 추천 장학금 상세
]