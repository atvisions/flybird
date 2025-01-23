# Generated by Django 4.2.17 on 2025-01-22 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("template_editor", "0003_remove_template_canvas_data_template_pages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="template",
            name="status",
            field=models.SmallIntegerField(
                choices=[(0, "草稿"), (1, "已发布"), (2, "待审核"), (3, "已下架")],
                default=0,
                verbose_name="状态",
            ),
        ),
    ]
