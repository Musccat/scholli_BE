from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .iamport import Iamport
from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

# 결제 페이지를 렌더링하는 뷰
def payment_page(request):
    permission_classes = [IsAuthenticated]
    merchant_code = settings.MERCHANT_CODE 
    return render(request, 'payment.html', {'merchant_code': merchant_code})

class PaymentView(APIView):
    def post(self, request):
        imp_uid = request.data.get('imp_uid')  # 클라이언트에서 전송한 imp_uid
        merchant_uid = request.data.get('merchant_uid')

        if not imp_uid or not merchant_uid:
            return Response({"error": "결제 정보가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # Iamport 인스턴스 초기화
        imp_key = settings.IMP_KEY
        imp_secret = settings.IMP_SECRET
        iamport = Iamport(imp_key=imp_key, imp_secret=imp_secret)

        try:
            # Iamport에서 결제 상태 조회
            response = iamport.find_by_imp_uid(imp_uid=imp_uid)

            # 결제가 성공 상태인지 확인
            if response['status'] == 'paid':
                # 결제 정보를 저장
                payment = Payment.objects.create(
                    user=request.user,
                    amount=response['amount'],
                    merchant_uid=merchant_uid,
                    imp_uid=imp_uid,
                    status='paid',
                    payment_time=timezone.now()
                )
                return Response({"message": "결제가 성공적으로 완료되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "결제 실패: 결제가 완료되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        except Iamport.ResponseError as e:
            return Response({"error": f"Iamport 오류: {e.message}"}, status=status.HTTP_400_BAD_REQUEST)
        except Iamport.HttpError as e:
            return Response({"error": f"HTTP 오류: {e.reason}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentCallbackView(APIView):
    def post(self, request):
        imp_uid = request.data.get('imp_uid')
        merchant_uid = request.data.get('merchant_uid')

        if not imp_uid or not merchant_uid:
            return Response({"error": "결제 정보가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # Iamport 인스턴스 초기화
        imp_key = settings.IMP_KEY
        imp_secret = settings.IMP_SECRET
        iamport = Iamport(imp_key=imp_key, imp_secret=imp_secret)

        try:
            # Iamport에서 결제 상태 조회
            response = iamport.find_by_imp_uid(imp_uid=imp_uid)

            # 결제가 성공 상태인지 확인
            if response['status'] == 'paid':
                # 결제 정보를 저장
                payment = Payment.objects.create(
                    user=request.user,  # 또는 유저 정보를 결제정보에서 가져옴
                    amount=response['amount'],
                    merchant_uid=merchant_uid,
                    imp_uid=imp_uid,
                    status='paid',
                    payment_time=timezone.now()
                )
                return Response({"message": "결제가 성공적으로 완료되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "결제 실패: 결제가 완료되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        except Iamport.ResponseError as e:
            return Response({"error": f"Iamport 오류: {e.message}"}, status=status.HTTP_400_BAD_REQUEST)
        except Iamport.HttpError as e:
            return Response({"error": f"HTTP 오류: {e.reason}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
