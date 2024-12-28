from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('users', '前一个迁移'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='type',
            field=models.CharField(
                choices=[
                    ('project', '项目'),
                    ('website', '网站'),
                    ('app', '应用'),
                    ('article', '文章'),
                    ('other', '其他')
                ],
                default='project',
                max_length=20,
                verbose_name='作品类型'
            ),
        ),
        migrations.AlterModelOptions(
            name='portfolio',
            options={
                'ordering': ['-created_at'],
                'verbose_name': '作品集',
                'verbose_name_plural': '作品集'
            },
        ),
    ] 