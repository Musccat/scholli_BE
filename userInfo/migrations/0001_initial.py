import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scholarships', '0004_alter_scholarship_financial_aid_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('univ_category', models.CharField(choices=[('4년제(5~6년제)', '4년제(5~6년제)'), ('전문대(2~3년제)', '전문대(2~3년제)'), ('해외대학', '해외대학'), ('학점은행제 대학', '학점은행제 대학'), ('원격대학', '원격대학'), ('기술대학', '기술대학')], default='4년제(5~6년제)', max_length=50)),
                ('gender', models.CharField(choices=[('남성', '남성'), ('여성', '여성'), ('선택안함', '선택안함')], default='선택안함', max_length=10)),
                ('age', models.SmallIntegerField()),
                ('university', models.CharField(max_length=100)),
                ('semester', models.CharField(choices=[('대학신입생', '대학신입생'), ('2학기', '2학기'), ('3학기', '3학기'), ('4학기', '4학기'), ('5학기', '5학기'), ('6학기', '6학기'), ('7학기', '7학기'), ('대학 8학기이상', '대학 8학기이상')], max_length=10, null=True)),
                ('major_category', models.CharField(choices=[('공학계열', '공학계열'), ('교육계열', '교육계열'), ('사회계열', '사회계열'), ('예체능계열', '예체능계열'), ('의약계열', '의약계열'), ('인문계열', '인문계열'), ('자연계열', '자연계열')], max_length=50)),
                ('major', models.CharField(max_length=100)),
                ('totalGPA', models.DecimalField(decimal_places=2, max_digits=3)),
                ('income', models.PositiveIntegerField()),
                ('residence', models.CharField(max_length=100)),
                ('etc', models.TextField(blank=True, null=True)),
                ('username', models.OneToOneField(db_column='username', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('scholarship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholarships.scholarship')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='wishlist',
            constraint=models.UniqueConstraint(fields=('user', 'scholarship'), name='unique_user_scholarship'),
        ),
    ]
