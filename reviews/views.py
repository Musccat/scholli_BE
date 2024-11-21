from reviews.models import Review
from scholarships.models import Scholarship
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from reviews.serializers import ReviewSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from payment.utils import subscription_required
from userInfo.models import UserSubscription

class ReviewList(APIView):
    def get(self, request, product_id):
        try:
            # product_id를 기반으로 해당 장학금을 찾음
            scholarship = Scholarship.objects.get(product_id=product_id)
        except Scholarship.DoesNotExist:
            # 장학금을 찾을 수 없는 경우 예외 처리
            raise Http404("해당 장학금을 찾을 수 없습니다.")

        # 해당 장학금에 대한 리뷰들을 불러옴
        reviews = Review.objects.filter(scholarship=scholarship).order_by("-id")

        # 구독 상태 확인
        is_subscribed = False
        if request.user.is_authenticated:
            try:
                subscription = UserSubscription.objects.get(user=request.user)
                subscription.check_subscription_status()  # 구독 상태 확인
                is_subscribed = subscription.is_active
            except UserSubscription.DoesNotExist:
                pass

        # 리뷰 데이터를 구독 상태에 따라 처리
        serialized_reviews = []
        for review in reviews:
            serialized_reviews.append({
                "id": review.id,
                "user": {
                    "username": review.user.username,
                },
                "income": review.income if is_subscribed else "*분위",
                "totalGPA": review.totalGPA if is_subscribed else "*.**",
                "univCategory": review.univCategory if is_subscribed else "*년제",
                "semesterCategory": review.semesterCategory if is_subscribed else "대학*학기",
                "majorCategory": review.majorCategory if is_subscribed else "**계열",
                "year": review.year,
                # 구독 여부에 따라 advice와 interviewTip 처리
                "advice": review.advice if is_subscribed else "*" * len(review.advice),
                "interviewTip": review.interviewTip if is_subscribed else "*" * len(review.interviewTip),
            })

        # 응답 데이터 구성
        response_data = {
            "is_subscribed": is_subscribed,
            "reviews": serialized_reviews,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.data)
        #product_id = request.data.get('id')
        product_id = request.data.get('scholarship', {}).get('id')
        if not product_id:
            return Response({"error": "product_id가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scholarship = Scholarship.objects.get(product_id=product_id)
        except Scholarship.DoesNotExist:
            return Response({"error": "해당 장학금이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            # 장학금과 현재 요청의 유저를 연결하여 저장
            serializer.save(scholarship=scholarship, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    def put(self, request, review_pk):
        review = get_object_or_404(Review, id=review_pk)
        if request.user == review.user:
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk, review_pk):
        review=get_object_or_404(Review, id=review_pk)
        if request.user==review.user:
            review.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


class FoundationListAPIView(APIView):
    def get(self, request):
        foundations = Scholarship.objects.values('foundation_name').distinct()
        foundation_list = [
            {
                'name':foundation['foundation_name']
            }
            for foundation in foundations if foundation['foundation_name']
        ]
        return Response(foundation_list)
    

class ScholarshipByFoundationAPIView(APIView):
    def get(self, request, foundationName):
        scholarships = Scholarship.objects.filter(foundation_name=foundationName)
        scholarlist = [
            {
                'name':scholarship.name,
                'id': scholarship.product_id,  
            }
            for scholarship in scholarships
        ]
        return Response(scholarlist)

#선택한 거 줘 추가하기 (장학금명, product_id)
class ScholarshipProductView(APIView):
    def get(self, request):
        # Query parameters로 foundation_name과 scholarship_name 받기
        foundation_name = request.query_params.get('foundation_name')
        scholarship_name = request.query_params.get('name')

        # 필수 값 체크
        if not foundation_name or not scholarship_name:
            return Response({"error": "foundation_name and scholarship_name are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Scholarship 모델에서 해당 재단명과 장학금명으로 데이터 검색
            scholarship = Scholarship.objects.get(foundation_name=foundation_name, name=scholarship_name)
            # 요청한 장학금의 이름과 product_id를 반환
            return Response({
                "name": scholarship.name,
                "product_id": scholarship.product_id,
            }, status=status.HTTP_200_OK)
        except Scholarship.DoesNotExist:
            return Response({"error": "No matching scholarship found."}, status=status.HTTP_404_NOT_FOUND)