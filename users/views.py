from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django_redis import get_redis_connection
from redis import Redis
from .utils import sendEmailHelper
from users.models import User
from users.serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from .tasks import send_email 

#JWT 토큰 발급
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

#아이디 중복 검사
class CheckUsernameAvailability(APIView):
    permission_classes = [AllowAny]
    def get(self, request, username):
        # 'username' 파라미터로 받은 값이 User 모델에 존재하는지 확인
        is_available = not User.objects.filter(username=username).exists()
        return Response({'available': is_available}, status=status.HTTP_200_OK)

#사용자 등록
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error":"Email is required for registration"}, status=status.HTTP_400_BAD_REQUEST)

        client = get_redis_connection("default") 
        verification_status = client.get(email)
        if verification_status is None:
            return Response({"error":"Email not verified or verification expired"}, status=status.HTTP_400_BAD_REQUEST)
        if verification_status.decode("utf-8") != "true":
            return Response({"error":"Email not verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = super().create(request, *args, **kwargs)

        client.delete(email)
        return response

#API 기본 라우트를 리스트로 반환
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/users/login/',
        '/users/register/',
        '/users/token/refresh/'
    ]
    return Response(routes)

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

#사용자 프로필 정보 조회 및 업데이트
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    #serializer_class = UserProfileSerializer

    #def get(self, request, *args, **kwargs):
        #serializer = self.serializer_class(request.user)
        #return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request):

        #user = get_object_or_404(User, id=user_id)
        #serializer = UserProfileSerializer(user)
        user = request.user
        serializer = UserProfileSerializer(user)
        print(serializer.data)

        return Response(serializer.data)
    

    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("안녕")
        return Response(serializer.data, status=status.HTTP_200_OK)


# class SendVerificationCodeView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = EmailVerificationSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             verification, created = EmailVerification.objects.get_or_create(email=email)
#             verification.generate_verification_code()

#             # 인증번호를 포함한 이메일 전송
#             send_mail(
#                 subject='Your Verification Code',  # 이메일 제목
#                 message=f'Your verification code is {verification.verification_code}.',  # 이메일 내용
#                 from_email=settings.DEFAULT_FROM_EMAIL,  # 발신자 이메일 (settings.py에 설정 필요)
#                 recipient_list=[email],  # 수신자 이메일
#                 fail_silently=False,  # 에러 발생 시 예외를 발생시킵니다.
#             )

#             return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VerifyCodeView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = VerifyCodeSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             entered_code = serializer.validated_data['verify_code']

#             try:
#                 # 이메일로 저장된 인증번호 가져오기
#                 verification = EmailVerification.objects.get(email=email)

#                 # 인증번호 유효성 검사
#                 if verification.verification_code == entered_code and verification.is_code_valid():
#                     return Response({"valid": True}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"valid": False, "message": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)
#             except EmailVerification.DoesNotExist:
#                 return Response({"valid": False, "message": "No verification code found for this email."}, status=status.HTTP_404_NOT_FOUND)

#         return Response({"valid": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmailVerifyView(APIView):
    permission_classes = [AllowAny]
    client = get_redis_connection("default") 

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        try:
            send_email.delay(email)
            return Response({"detail":"Success to send Email"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e : 
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        code = request.data.get("verify-code")
        email = request.data.get("email")
        if not code or not email:
            return Response({"valid":False, "error": "Email and code are required"}, status=status.HTTP_400_BAD_REQUEST)

        answer = self.client.get(email)
        if code == answer.decode("utf-8"):
            self.client.delete(email)
            self.client.set(email, "true", ex=86400)
            return Response({"valid": True}, status=status.HTTP_200_OK)
        else : 
            return Response({"valid": False, "error": "Code Not Matched"}, status=status.HTTP_400_BAD_REQUEST)
