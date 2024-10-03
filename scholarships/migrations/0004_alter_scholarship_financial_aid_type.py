# Generated by Django 5.0.7 on 2024-09-07 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0003_scholarship_academic_year_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='financial_aid_type',
            field=models.CharField(choices=[('지역연고', '지역연고'), ('성적우수', '성적우수'), ('소득구분', '소득구분'), ('특기자', '특기자'), ('기타', '기타')], max_length=20, null=True),
        ),
    ]