from users.models import User
from django.db import models
from scholarships.models import Scholarship
from django.contrib.auth import get_user_model
from django.utils import timezone

class Profile(models.Model):
    
    SEMESTER_CATEGORIES = [
        ('대학신입생', '대학신입생'),
        ('대학2학기', '대학2학기'),
        ('대학3학기', '대학3학기'),
        ('대학4학기', '대학4학기'),
        ('대학5학기', '대학5학기'),
        ('대학6학기', '대학6학기'),
        ('대학7학기', '대학7학기'),
        ('대학8학기이상', '대학8학기이상'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 
    univ_category = models.CharField(max_length=255, choices=[('4년제(5~6년제포함)', '4년제(5~6년제포함)'), ('전문대(2~3년제)', '전문대(2~3년제)'), ('해외대학', '해외대학'), ('학점은행제 대학', '학점은행제 대학'), ('원격대학', '원격대학'), ('기술대학', '기술대학')], default='4년제(5~6년제포함)', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('남성', '남성'), ('여성', '여성'), ('선택안함', '선택안함')], default='선택안함', null=True, blank=True)
    age = models.SmallIntegerField(null=True, blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    semester = models.CharField(max_length=10, choices=SEMESTER_CATEGORIES, null=True, blank=True)
    major_category = models.CharField(max_length=50, choices=[('공학계열', '공학계열'), ('교육계열', '교육계열'), ('사회계열', '사회계열'), ('예체능계열', '예체능계열'), ('의약계열', '의약계열'), ('인문계열', '인문계열'), ('자연계열', '자연계열')], null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    totalGPA = models.CharField(max_length=10, null=True, blank=True)
    income = models.CharField(max_length=10, null=True, blank=True)
    residence = models.CharField(max_length=100, null=True, blank=True)
    etc = models.TextField(blank=True, null=True)  # 기타 사항

    def __str__(self):
        return self.user.username if self.user else "No User"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'scholarship'], name='unique_user_scholarship')
        ]
    def __str__(self):
        return f"{self.user.username}의 관심 목록 - {self.scholarship.name}"
    

class RecommendResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommended_scholarships')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=50, null=True, blank=True, default='unknown')
    recommended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}에게 추천된 {self.scholarship.name}"
    
# User = get_user_model()

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    is_active = models.BooleanField(default=False)  # 구독 상태
    expiration_date = models.DateTimeField(null=True, blank=True)  # 구독 만료일

    def activate_subscription(self):
        self.is_active = True
        self.expiration_date = timezone.now() + timezone.timedelta(days=31)  # 1개월 구독
        self.save()

    def check_subscription_status(self):
        # 구독 만료일이 지났으면 비활성화
        if self.expiration_date and self.expiration_date < timezone.now():
            self.is_active = False
            self.save()