# Generated by Django 4.2.17 on 2025-01-22 18:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("template_editor", "0004_alter_template_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="template",
            name="liked_by",
            field=models.ManyToManyField(
                blank=True,
                related_name="liked_templates",
                to=settings.AUTH_USER_MODEL,
                verbose_name="点赞用户",
            ),
        ),
        migrations.AddField(
            model_name="template",
            name="likes",
            field=models.PositiveIntegerField(default=0, verbose_name="点赞数"),
        ),
        migrations.AddField(
            model_name="template",
            name="views",
            field=models.PositiveIntegerField(default=0, verbose_name="浏览次数"),
        ),
    ]
