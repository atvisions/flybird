# Generated by Django 4.2.17 on 2025-01-10 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_options_user_avatar_user_background_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_vip",
            field=models.BooleanField(default=False, verbose_name="是否是VIP用户"),
        ),
    ]
