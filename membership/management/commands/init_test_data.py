from django.core.management.base import BaseCommand
from membership.models import MembershipTier

class Command(BaseCommand):
    help = '创建测试数据'

    def handle(self, *args, **kwargs):
        # 创建会员等级
        tier, _ = MembershipTier.objects.get_or_create(
            name='高级会员',
            defaults={
                'tier_type': 'premium',
                'price_monthly': 29.9,
                'price_quarterly': 79.9,
                'price_yearly': 299.9,
                'description': '解锁全部高级功能',
                'sort_order': 1
            }
        )
        self.stdout.write(self.style.SUCCESS('创建会员等级成功')) 