from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('users', '前一个迁移文件'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='总分')),
                ('basic_dimension', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='基础维度')),
                ('experience_dimension', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='经验维度')),
                ('ability_dimension', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='能力维度')),
                ('achievement_dimension', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='成就维度')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_score', to='users.user')),
            ],
            options={
                'verbose_name': '档案评分',
                'verbose_name_plural': '档案评分',
            },
        ),
    ] 