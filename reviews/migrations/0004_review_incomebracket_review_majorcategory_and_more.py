# Generated by Django 5.0.7 on 2024-09-02 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_rename_benefit_tip_review_advice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='incomeBracket',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='majorCategory',
            field=models.CharField(choices=[('공학계열', '공학계열'), ('교육계열', '교육계열'), ('사회계열', '사회계열'), ('예체능계열', '예체능계열'), ('의약계열', '의약계열'), ('인문계열', '인문계열'), ('자연계열', '자연계열')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='semesterCategory',
            field=models.CharField(choices=[('대학신입생', '대학신입생'), ('2학기', '2학기'), ('3학기', '3학기'), ('4학기', '4학기'), ('5학기', '5학기'), ('6학기', '6학기'), ('7학기', '7학기'), ('대학 8학기이상', '대학 8학기이상')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='totalGPA',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='univCategory',
            field=models.CharField(choices=[('4년제(5~6년제)', '4년제(5~6년제)'), ('전문대(2~3년제)', '전문대(2~3년제)'), ('해외대학', '해외대학'), ('학점은행제 대학', '학점은행제 대학'), ('원격대학', '원격대학'), ('기술대학', '기술대학')], max_length=10, null=True),
        ),
    ]