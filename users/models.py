from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date, timedelta, datetime
import random, string
from django.utils import timezone



class User(AbstractUser):
    nickname = models.CharField(max_length=50, null=False, blank=False, default="nonickname")
    birth = models.DateField(null=False, blank=False, default=date(1900,1,1))
    fullname = models.CharField(max_length=10, null=False, blank=False, default="nofullname")

    def __str__(self):
        return self.nickname


class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)  # 인증번호 생성 시간 추가
    expiration_time = models.DateTimeField()  # 인증번호 만료 시간

    def generate_verification_code(self):
        self.verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self.expiration_time = datetime.now() + timedelta(minutes=2)
        self.save()

    def is_code_valid(self):
        # 현재 시간이 만료 시간 이전이면 True, 아니면 False
        return datetime.now() < self.expiration_time

    def __str__(self):
        return f"{self.email} - {self.verification_code} (Expires: {self.expiration_time})"