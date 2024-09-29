from rest_framework import serializers
from .models import Profile, Wishlist
from users.models import User

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    nickname = serializers.SerializerMethodField()

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

