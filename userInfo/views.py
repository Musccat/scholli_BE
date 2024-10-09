from rest_framework import generics, permissions, status
from .models import Profile, Wishlist
from scholarships.models import Scholarship
from .serializers import ProfileSerializer, WishlistSerializer, UserInfoScholarshipSerializer, RecommendResultSerializer, AllInfoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import RecommendResult
from .utils import filter_scholarships_by_date, filter_basic, gpt_filter_region, recommend_scholarships,  separate_scholarships
from rest_framework.exceptions import ValidationError, NotFound 
from django.utils.dateparse import parse_date
from datetime import datetime, date
import openai
import re
from django.core.exceptions import ObjectDoesNotExist

def calculate_age(birth_date):
    if birth_date:
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    else:
        return 0

class ProfileCreateView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            # 현재 로그인된 사용자의 프로필을 반환
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return Profile.objects.create(user=self.request.user, age = calculate_age(self.request.user.birth))
    
    # def perform_create(self, serializer):
    #     birth_date = self.request.user.birth
    #     age = calculate_age(birth_date)
    #     serializer.save(username=self.request.user.username, age=age)
    
    def perform_update(self, serializer):
        birth_date = self.request.user.birth
        age = calculate_age(birth_date)
        serializer.save(user=self.request.user, age=age)
    
class AllInfoView(generics.RetrieveAPIView):
    serializer_class = AllInfoSerializer
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def get_object(self):
        # 현재 로그인된 사용자의 Profile 객체를 반환, 없으면 생성
        profile, created = Profile.objects.get_or_create(
            user=self.request.user,  # user 외래키는 현재 로그인된 사용자로 설정
            defaults={
                'univ_category': None,
                'gender': None,
                'age': None,
                'university': None,
                'semester': None,
                'major_category': None,
                'major': None,
                'totalGPA': None,
                'income': None,
                'residence': None,
                'etc': None
            }
        )
        return profile

# 찜 추가
class WishlistCreateView(generics.CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.request.data.get('scholarship_id')  # 클라이언트에서 전달받은 product_id
        try:
            scholarship = Scholarship.objects.get(product_id=product_id)
            serializer.save(user=user, scholarship=scholarship)
        except Scholarship.DoesNotExist:
            return Response({"error": "해당 장학금을 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

# 찜 삭제
class WishlistDeleteView(generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        product_id = self.kwargs['scholarship_id']  # URL에서 받은 product_id
        try:
            scholarship = Scholarship.objects.get(product_id=product_id)
            wishlist_item = Wishlist.objects.get(user=user, scholarship=scholarship)
            wishlist_item.delete()
            return Response({"message": "찜 목록에서 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except Scholarship.DoesNotExist:
            return Response({"error": "해당 장학금을 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Wishlist.DoesNotExist:
            return Response({"error": "찜 목록에 해당 장학금이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

# 찜 목록 조회
class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

# 장학금 추천 뷰 (POST 요청으로 날짜를 받아 처리)
class RecommendScholarshipsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoScholarshipSerializer

    def post(self, request):
        # 현재 로그인된 사용자 프로필
        user_profile = Profile.objects.get(user=self.request.user)

        # 클라이언트에서 POST로 받은 날짜
        current_date_input = request.data.get('date')
        if not current_date_input:
            return Response({"error": "날짜를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_date = datetime.strptime(current_date_input, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "잘못된 날짜 형식입니다. YYYY-MM-DD 형식으로 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. 모집 날짜 필터링
        scholarships = Scholarship.objects.all()
        scholarships = filter_scholarships_by_date(current_date, scholarships)
        print(f"1. 모집 날짜 필터링 결과 개수: {scholarships.count()}")

        # 2. 대학, 학과, 학년 구분 필터링
        scholarships = filter_basic(scholarships, user_profile)
        print(f"2. 대학, 학과, 학년 필터링 결과 개수: {scholarships.count()}")

        # 3. 장학금 분리 (해당없음 vs. 해당없음이 아닌 장학금)
        no_criteria_scholarships, criteria_scholarships = separate_scholarships(scholarships)
        print(f"해당없음 장학금 개수: {no_criteria_scholarships.count()}")
        print(f"해당없음이 아닌 장학금 개수: {criteria_scholarships.count()}")

        # 4. GPT로 지역 필터링
        filtered_ids = gpt_filter_region(user_profile, criteria_scholarships)
        print(f"3. GPT로 지역 필터링 결과 ID 개수: {len(filtered_ids)}")

        # 5. GPT로 필터링된 장학금과 '해당없음' 장학금 합치기
        filtered_scholarships = criteria_scholarships.filter(product_id__in=filtered_ids)
        final_scholarships = filtered_scholarships | no_criteria_scholarships
        print(f"합친 개수: {final_scholarships.count()}")
        print(f"필터링된 장학금: {filtered_scholarships.count()}")
        print(f"해당없음 장학금: {no_criteria_scholarships.count()}")
        print(f"합친 장학금: {[s.product_id for s in final_scholarships]}")

        # 6. GPT로 나머지 조건 필터링 및 추천
        recommended_ids = recommend_scholarships(user_profile, final_scholarships)
        print(f"4. GPT 추천 결과 ID 개수: {len(recommended_ids)}")
        print(f"GPT 추천 결과 IDs: {recommended_ids}")

        # 최종 필터링된 장학금 반환
        final_scholarships = final_scholarships.filter(product_id__in=recommended_ids)

        # 7. 추천된 장학금을 DB에 저장
        for scholarship in final_scholarships:
            # 이미 저장된 추천 기록이 있는지 확인
            recommended_scholarship, created = RecommendResult.objects.get_or_create(
                user=user_profile.user,
                scholarship=scholarship,
                product_id=scholarship.product_id
            )
            if created:
                print(f"장학금 {scholarship.name}이(가) {user_profile.user.username}에게 추천되었습니다.")

        serializer = self.get_serializer(final_scholarships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RecommendScholarListView(generics.ListAPIView):
    serializer_class = RecommendResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = Profile.objects.get(user=self.request.user)
        #user = user_profile.username
        return RecommendResult.objects.filter(user=user_profile.user)
    
class RecommendScholarshipsDetail(generics.RetrieveAPIView):
    queryset = Scholarship.objects.all()
    serializer_class = UserInfoScholarshipSerializer
    permission_classes = [IsAuthenticated]

    # product_id를 기준으로 장학금 찾기
    def get_object(self):
        product_id = self.kwargs['product_id']
        try:
            return Scholarship.objects.get(product_id=product_id)
        except Scholarship.DoesNotExist:
            raise NotFound("해당 장학금을 찾을 수 없습니다.")