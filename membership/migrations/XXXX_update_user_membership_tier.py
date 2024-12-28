from django.db import migrations, models
from django.db.models import Q

def set_default_tier(apps, schema_editor):
    """设置默认会员等级"""
    MembershipTier = apps.get_model('membership', 'MembershipTier')
    UserMembership = apps.get_model('membership', 'UserMembership')
    
    # 获取默认会员等级
    default_tier = MembershipTier.objects.filter(
        Q(is_default=True) | Q(tier_type='free')
    ).first()
    
    if not default_tier:
        # 如果没有默认等级，创建一个
        default_tier = MembershipTier.objects.create(
            name='普通用户',
            tier_type='free',
            price_monthly=0,
            price_quarterly=0,
            price_yearly=0,
            is_default=True,
            description='基础功能使用',
            sort_order=0
        )
    
    # 更新所有没有等级的会员
    UserMembership.objects.filter(tier__isnull=True).update(tier=default_tier)

def reverse_func(apps, schema_editor):
    """回滚操作"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),  # 需要替换为你的实际依赖
    ]

    operations = [
        migrations.RunPython(set_default_tier, reverse_func),
        migrations.AlterField(
            model_name='usermembership',
            name='tier',
            field=models.ForeignKey(
                on_delete=models.PROTECT,
                to='membership.MembershipTier',
                verbose_name='会员等级'
            ),
        ),
    ] 