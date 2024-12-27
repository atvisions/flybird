from django.db import migrations

def create_default_tiers(apps, schema_editor):
    MembershipTier = apps.get_model('membership', 'MembershipTier')
    
    # 创建免费会员等级
    MembershipTier.objects.create(
        name='免费用户',
        tier_type='free',
        price_monthly=0,
        price_quarterly=0,
        price_yearly=0,
        is_default=True,
        description='基础功能免费使用',
        sort_order=0
    )
    
    # 创建高级会员等级
    MembershipTier.objects.create(
        name='高级会员',
        tier_type='premium',
        price_monthly=29.9,
        price_quarterly=79.9,
        price_yearly=299.9,
        is_default=False,
        description='解锁全部高级功能',
        sort_order=1
    )

def delete_default_tiers(apps, schema_editor):
    MembershipTier = apps.get_model('membership', 'MembershipTier')
    MembershipTier.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_default_tiers,
            delete_default_tiers
        ),
    ] 