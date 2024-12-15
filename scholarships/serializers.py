from rest_framework import serializers
from .models import Scholarship

class ScholarshipSerializer(serializers.ModelSerializer):
    is_in_wishlist = serializers.BooleanField()

    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ['product_id']  # product_id는 자동으로 생성되므로 읽기 전용
