# Generated by Django 5.0.7 on 2024-09-18 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0004_alter_scholarship_financial_aid_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='gpt_interview_tips',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='gpt_success_tips',
            field=models.TextField(blank=True, null=True),
        ),
    ]
