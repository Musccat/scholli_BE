from users.models import User
from django.db import models
from scholarships.models import Scholarship

class Profile(models.Model):
    
    SEMESTER_CATEGORIES = [
        ('대학신입생', '대학신입생'),
        ('2학기', '2학기'),
        ('3학기', '3학기'),
        ('4학기', '4학기'),
        ('5학기', '5학기'),
        ('6학기', '6학기'),
        ('7학기', '7학기'),
        ('대학 8학기이상', '대학 8학기이상'),
    ]

    username = models.OneToOneField(User, on_delete=models.CASCADE, db_column='username', to_field='username')
    univ_category = models.CharField(max_length=50, choices=[('4년제(5~6년제)', '4년제(5~6년제)'), ('전문대(2~3년제)', '전문대(2~3년제)'), ('해외대학', '해외대학'), ('학점은행제 대학', '학점은행제 대학'), ('원격대학', '원격대학'), ('기술대학', '기술대학')], default='4년제(5~6년제)')
    gender = models.CharField(max_length=10, choices=[('남성', '남성'), ('여성', '여성'), ('선택안함', '선택안함')], default='선택안함')
    age = models.SmallIntegerField()
    university = models.CharField(max_length=100)
    semester = models.CharField(max_length=10, choices=SEMESTER_CATEGORIES, null=True)
    major_category = models.CharField(max_length=50, choices=[('공학계열', '공학계열'), ('교육계열', '교육계열'), ('사회계열', '사회계열'), ('예체능계열', '예체능계열'), ('의약계열', '의약계열'), ('인문계열', '인문계열'), ('자연계열', '자연계열')])
    major = models.CharField(max_length=100)
    totalGPA = models.DecimalField(max_digits=3, decimal_places=2) 
    income = models.PositiveIntegerField()
    residence = models.CharField(max_length=100)
    etc = models.TextField(blank=True, null=True)  # 기타 사항

    def __str__(self):
        return self.username.username

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