from rest_framework import generics, permissions, status
from .models import Profile, Wishlist
from scholarships.models import Scholarship
from .serializers import ProfileSerializer, WishlistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
        # 현재 로그인된 사용자의 프로필을 반환
        return Profile.objects.get(username=self.request.user)
    

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

