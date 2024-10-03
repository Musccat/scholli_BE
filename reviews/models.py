from django.db import models
from users.models import User
from scholarships.models import Scholarship

# Create your models here.
class Review(models.Model):

    UNIVERSITY_CATEGORIES = [
        ('4년제(5~6년제)', '4년제(5~6년제)'),
        ('전문대(2~3년제)', '전문대(2~3년제)'),
        ('해외대학', '해외대학'),
        ('학점은행제 대학', '학점은행제 대학'),
        ('원격대학', '원격대학'),
        ('기술대학', '기술대학'),
    ]

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

    MAJOR_CATEGORIES = [
        ('공학계열', '공학계열'),
        ('교육계열', '교육계열'),
        ('사회계열', '사회계열'),
        ('예체능계열', '예체능계열'),
        ('의약계열', '의약계열'),
        ('인문계열', '인문계열'),
        ('자연계열', '자연계열'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    income = models.CharField(max_length=10, null=True)
    totalGPA = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    univCategory = models.CharField(max_length=10, choices=UNIVERSITY_CATEGORIES, null=True)
    semesterCategory = models.CharField(max_length=10, choices=SEMESTER_CATEGORIES, null=True)
    majorCategory = models.CharField(max_length=10, choices=MAJOR_CATEGORIES, null=True)
    year = models.SmallIntegerField(default='0')
    advice = models.TextField()
    interviewTip =  models.TextField()

   