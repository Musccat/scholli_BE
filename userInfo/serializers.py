from rest_framework import serializers
from .models import Profile, Wishlist, RecommendResult
from users.models import User
from scholarships.models import Scholarship

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)
    nickname = serializers.SerializerMethodField()  # User 모델의 nickname을 가져오기 위한 필드
    age = serializers.IntegerField(required=False)

    class Meta:
        model = Profile
        fields = [
            'username', 'nickname', 'univ_category', 'gender', 'age', 'university', 
            'semester', 'major_category', 'major', 'totalGPA', 
            'income', 'residence', 'etc'
        ]

    # User 모델의 nickname을 가져오는 메서드
    def get_nickname(self, obj):
        return obj.user.nickname if obj.user else None
    
    def create(self, validated_data):
        validated_data['username'] = self.context['request'].user.username
        validated_data['age'] = calculate_age(self.context['request'].user.birth)
        return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

class AllInfoSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)
    fullname = serializers.CharField(source='user.fullname', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    birth = serializers.DateField(source='user.birth', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model=Profile
        fields = [
            'username', 'fullname', 'nickname', 'birth', 'email', 'univ_category', 'gender', 'age', 'university', 'semester', 'major_category', 'major', 'totalGPA', 'income', 'residence', 'etc'
        ]



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