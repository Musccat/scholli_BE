from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
import random, string

class User(AbstractUser):
    nickname = models.CharField(max_length=50, null=False, blank=False, default="nonickname")
    birth = models.DateField(null=False, blank=False, default=date(1900,1,1))
    fullname = models.CharField(max_length=10, null=False, blank=False, default="nofullname")

    def __str__(self):
        return self.nickname


class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=6)

    def generate_verification_code(self):
        self.verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self.save()

    def __str__(self):
        return f"{self.email} - {self.verification_code}"