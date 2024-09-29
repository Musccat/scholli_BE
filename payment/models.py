from django.db import models
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant_uid = models.CharField(max_length=255)
    imp_uid = models.CharField(max_length=255, unique=True)  # imp_uid 필드 추가
    status = models.CharField(max_length=20)
    payment_time = models.DateTimeField()

    def __str__(self):
        return f"{self.merchant_uid} - {self.amount} - {self.status}"
