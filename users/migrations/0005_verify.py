# Generated by Django 5.0.7 on 2024-08-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_birth_alter_user_fullname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('athnt_code', models.CharField(max_length=6)),
            ],
        ),
    ]
