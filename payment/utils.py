from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from userInfo.models import UserSubscription

def subscription_required(view_func):
    @wraps(view_func)
    def _wrapped_view(view, *args, **kwargs):
        # CBV에서는 self가 첫 번째 매개변수로 전달됨
        request = view.request if hasattr(view, 'request') else args[0]
        
        # 사용자 인증 확인
        if not request.user.is_authenticated:
            return Response(
                {"error": "이 기능을 사용하려면 로그인해야 합니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        try:
            subscription = UserSubscription.objects.get(user=request.user)
            subscription.check_subscription_status()  # 만료 상태 확인
            if not subscription.is_active:
                return Response(
                    {"error": "이 기능을 사용하려면 활성화된 구독이 필요합니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except UserSubscription.DoesNotExist:
            return Response(
                {"error": "구독 정보가 없습니다. 이 기능을 사용하려면 구독이 필요합니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return view_func(request, *args, **kwargs)

    return _wrapped_view

     