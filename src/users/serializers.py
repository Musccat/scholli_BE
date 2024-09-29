from users.models import User, EmailVerification
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.generics import get_object_or_404

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):  #토큰 생성 방식에 username, email 정보 추가
        token = super().get_token(user)
        token['username'] = user.username
        return token

#사용자 등록
class RegisterSerializer(serializers.ModelSerializer):  
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'last_login', 'date_joined', 'is_staff', 'fullname', 'nickname', 'birth')
    
    def validate(self, attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"})
        return attrs
    
    def create(self, validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            nickname=validated_data.get('nickname', ''),
            birth=validated_data.get('birth', '')
        )

        if 'fullname' in validated_data:
            user.fullname = validated_data['fullname']
        
        user.set_password(validated_data['password'])
        user.save()
        return user 
    
class UserProfileSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(
        #max_length=128,
        #min_length=8,
        #write_only=True
    #)
    class Meta:
        model = User
        fields = ('id', 'username', 'fullname', 'nickname', 'birth', 'email')

    
class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ['email']

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            verification = EmailVerification.objects.get(email=data['email'])
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid email address.")

        if verification.verification_code != data['verification_code']:
            raise serializers.ValidationError("Invalid verification code.")
        return data