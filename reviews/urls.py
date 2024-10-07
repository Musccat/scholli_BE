from django.contrib import admin
from django.urls import path, re_path
from reviews.views import ReviewList, ReviewDetailView, FoundationListAPIView, ScholarshipByFoundationAPIView, ScholarshipProductView


urlpatterns = [
    path('', ReviewList.as_view()),
    path('view/<str:product_id>/', ReviewList.as_view()),
    path('edit/<int:review_pk>/', ReviewDetailView.as_view()),
    path('foundations/', FoundationListAPIView.as_view()),
    re_path(r'^scholarships/(?P<foundationName>.+)/$', ScholarshipByFoundationAPIView.as_view(), name='scholarship-by-foundation'),
    #path('get-product-id/', ScholarshipProductView.as_view()),
]
