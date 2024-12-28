from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('users', '前一个迁移'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicinfo',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='出生日期'),
        ),
    ] 