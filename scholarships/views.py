from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Scholarship
from reviews.models import Review
from .serializers import ScholarshipSerializer, ScholarshipListSerializer
from .pagination import SetPagination
from .models import Scholarship
from .filters import ScholarshipFilter
from django_filters.rest_framework import DjangoFilterBackend
import openai
from django.conf import settings 
from .utils import extract_key_points_from_tips  # 공통 유틸리티 함수 불러오기
from django.db.models import IntegerField, Case, When, BooleanField
from django.db.models.functions import Cast
from userInfo.models import Wishlist

# 장학금 목록
class ScholarshipList(generics.ListAPIView):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # 검색 필터 추가
    filterset_class = ScholarshipFilter  # 필터셋 클래스 설정
    ordering_fields = ['recruitment_start', 'recruitment_end']  
    ordering = ['-recruitment_end'] # 기본 정렬: 모집 종료 최신순

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Scholarship.objects.annotate(
                is_in_wishlist=Case(
                    default=False,
                    output_field=BooleanField()
                )
            )

        wishlist_ids = Wishlist.objects.filter(user=user).values_list('scholarship_id', flat=True)

        return Scholarship.objects.annotate(
            is_in_wishlist=Case(
                When(id__in=wishlist_ids, then=True),
                default=False,
                output_field=BooleanField()
            )
        )

# 장학금 상세 정보와 GPT 팁을 반환하는 뷰
class ScholarshipDetail(generics.RetrieveAPIView):
    #queryset = Scholarship.objects.all()
    serializer_class = ScholarshipListSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'product_id'

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Scholarship.objects.annotate(
                is_in_wishlist=Case(
                    default=False,
                    output_field=BooleanField()
                )
            )
        wishlist_ids = Wishlist.objects.filter(user=user).values_list('scholarship_id', flat=True)
        return Scholarship.objects.annotate(
            is_in_wishlist=Case(
                When(id__in=wishlist_ids, then=True),
                default=False,
                output_field=BooleanField()
            )
        )

    def get(self, request, product_id):
        try:
            scholarship = self.get_queryset().get(product_id=product_id)
        except Scholarship.DoesNotExist:
            return Response({"error": "해당 장학금이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 저장된 GPT 팁이 있는 경우
        if scholarship.gpt_success_tips and scholarship.gpt_interview_tips:
            return Response({
                "scholarship": ScholarshipListSerializer(scholarship, context={'request': request}).data
            }, status=status.HTTP_200_OK)

        # 저장된 팁이 없는 경우: 리뷰를 기반으로 새로운 팁을 추출
        reviews = Review.objects.filter(scholarship=scholarship)
        if reviews.exists():
            advice_tips = "\n".join([review.advice for review in reviews])
            interview_tips = "\n".join([review.interviewTip for review in reviews])

            # GPT로 팁 추출
            tips = f"합격 팁: {advice_tips}\n면접 팁: {interview_tips}"
            gpt_tips = extract_key_points_from_tips(tips)

            print("GPT 응답: " + gpt_tips)

            # 추출된 팁을 저장
            success_tips = gpt_tips.split("합격 팁:")[1].split("면접 팁:")[0].strip()
            interview_tips = gpt_tips.split("면접 팁:")[1].strip()

            # 팁을 모델에 저장
            scholarship.gpt_success_tips = success_tips
            scholarship.gpt_interview_tips = interview_tips
            scholarship.save()

            return Response({
                "scholarship": ScholarshipListSerializer(scholarship, context={'request': request}).data
            }, status=status.HTTP_200_OK)
        else:
            # 리뷰가 없는 경우
            return Response({
                "scholarship": ScholarshipListSerializer(scholarship, context={'request': request}).data
            }, status=status.HTTP_200_OK)

# 장학금 등록
class ScholarshipCreateView(generics.CreateAPIView):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def perform_create(self, serializer):
        # product_id를 숫자형으로 캐스팅하여 가장 큰 값을 찾음
        last_scholarship = Scholarship.objects.annotate(
            product_id_as_int=Cast('product_id', IntegerField())
        ).order_by('-product_id_as_int').first()
        
        if last_scholarship and last_scholarship.product_id.isdigit():
            # 가장 마지막 product_id의 숫자에 1을 더해 새로운 product_id를 생성
            new_product_id = str(int(last_scholarship.product_id) + 1)
        else:
            # 장학금이 없거나 숫자형 product_id가 없을 경우 초기값 설정
            new_product_id = "3000"  # 처음부터 시작할 product_id

        # product_id 저장
        serializer.save(product_id=new_product_id)