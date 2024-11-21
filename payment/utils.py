from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from userInfo.models import UserSubscription

def subscription_required(view_func):
    @wraps(view_func)
    def _wrapped_view(view, *args, **kwargs):
        # 요청 객체 가져오기
        request = view.request if hasattr(view, 'request') else view

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

        return view_func(view, *args, **kwargs)
    return _wrapped_view
