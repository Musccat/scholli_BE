from django.urls import path, include
from . import views 
from users.views import ProfileView, SendVerificationCodeView, VerifyCodeView, CheckUsernameAvailability
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

#mypage_view = UserViewSet.as_view({
    #'get' : 'list',
    #'post' : 'create',
    #'put' : 'update',
    #'delete' : 'destroy',
#})

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.getRoutes),
    path('mypage/', ProfileView.as_view()),
    path('mypage/update', ProfileView.as_view()),
    path('send-verification-code/', SendVerificationCodeView.as_view()),
    path('verify-code/', VerifyCodeView.as_view()),
    path('check-username/<str:username>/', CheckUsernameAvailability.as_view(), name='check_username'),
]
