from rest_framework import serializers
from reviews.models import Review
from scholarships.models import Scholarship
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        #fields = ('id', 'nickname')
        fields = ['id']

class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = ['product_id', 'foundation_name', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    scholarship = ScholarshipSerializer(read_only=True) #중첩된 시리얼라이저

    class Meta:
        model = Review
        fields = ['user', 'scholarship', 'id', 'income', 'totalGPA', 'univCategory', 'semesterCategory', 'majorCategory', 'year', 'advice', 'interviewTip']



