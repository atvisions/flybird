# Generated by Django 4.2.7 on 2024-12-30 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-date_joined'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='birth_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='出生日期'),
        ),
        migrations.AlterModelTable(
            name='user',
            table='auth_user',
        ),
    ]