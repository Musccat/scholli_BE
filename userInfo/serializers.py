from rest_framework import serializers
from .models import Profile, Wishlist, RecommendResult
from users.models import User
from scholarships.models import Scholarship

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    age = serializers.IntegerField(required=False)

    class Meta:
        model = Profile
        fields = [
            'username', 'nickname', 'univ_category', 'gender', 'age', 'university', 
            'semester', 'major_category', 'major', 'totalGPA', 
            'income', 'residence', 'etc'
        ]

    def get_nickname(self, obj):
        return obj.username.nickname
    
    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class WishlistSerializer(serializers.ModelSerializer):
    scholarship_id = serializers.CharField(source='scholarship.product_id', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['user', 'scholarship_id', 'added_at']
        read_only_fields = ['user','added_at']

class UserInfoScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = '__all__'

class RecommendResultSerializer(serializers.ModelSerializer):
    # Scholarship의 전체 정보를 반환하기 위해 scholarship 필드를 UserInfoScholarshipSerializer로 변경
    scholarship = UserInfoScholarshipSerializer(read_only=True)
    product_id = serializers.CharField(source='scholarship.product_id', read_only=True)

    class Meta:
        model = RecommendResult
        fields = ['scholarship', 'product_id', 'recommended_at']