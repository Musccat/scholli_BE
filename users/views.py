from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from users.models import User, EmailVerification
from users.serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserProfileSerializer, EmailVerificationSerializer, VerifyCodeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets


#JWT 토큰 발급
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

#인증코드 생성 & 이메일 발송
class AthntCodeCreateView(APIView):
    def post(self, request):
        email = request.data.get("email", "")
        if User.objects.filter(email=email).exists:
            return Response(
                {"message":"이미 가입된 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        #athnt_code = str(randint(1, 999999)).zfill(6)
        #message = EmailMessage(
            #"SCHOLLI [Verification Code]",
            #f"인증코드 [{athnt_code}]",
            #"",
            #[email],
        #)
        #authen_Code = Verify(email=email, athnt_code=athnt_code)
        #authen_Code.save()
        #message.send()
        #return Response({"message":"이메일을 보냈습니다."}, status=status.HTTP_200_OK)

#사용자 등록
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

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


class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification, created = EmailVerification.objects.get_or_create(email=email)
            verification.generate_verification_code()

            # 인증번호를 포함한 이메일 전송
            send_mail(
                subject='Your Verification Code',  # 이메일 제목
                message=f'Your verification code is {verification.verification_code}.',  # 이메일 내용
                from_email=settings.DEFAULT_FROM_EMAIL,  # 발신자 이메일 (settings.py에 설정 필요)
                recipient_list=[email],  # 수신자 이메일
                fail_silently=False,  # 에러 발생 시 예외를 발생시킵니다.
            )

            return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            # 인증번호 검증을 위한 로직만 남깁니다.
            return Response({"valid": True}, status=status.HTTP_200_OK)
        return Response({"valid": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)