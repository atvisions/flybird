# Generated by Django 4.2.17 on 2024-12-25 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicinfo',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='basicinfo',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='basicinfo',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='personal_summary',
            field=models.TextField(blank=True, verbose_name='个人简介'),
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='years_of_experience',
            field=models.IntegerField(blank=True, null=True, verbose_name='工作年限'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='job_title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='职位'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]