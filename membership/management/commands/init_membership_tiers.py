from django.core.management.base import BaseCommand
from membership.models import MembershipTier

class Command(BaseCommand):
    help = '初始化会员等级数据'

    def handle(self, *args, **kwargs):
        # 创建免费会员
        free_tier, _ = MembershipTier.objects.get_or_create(
            name='免费会员',
            defaults={
                'tier_type': 'free',
                'price_monthly': 0,
                'price_quarterly': 0,
                'price_yearly': 0,
                'description': '基础功能使用',
                'sort_order': 0,
                'is_default': True
            }
        )
        self.stdout.write(self.style.SUCCESS(f'创建免费会员等级: {free_tier.name}'))

        # 创建高级会员
        premium_tier, _ = MembershipTier.objects.get_or_create(
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
        self.stdout.write(self.style.SUCCESS(f'创建高级会员等级: {premium_tier.name}'))

        # 创建专业会员
        pro_tier, _ = MembershipTier.objects.get_or_create(
            name='专业会员',
            defaults={
                'tier_type': 'premium',
                'price_monthly': 49.9,
                'price_quarterly': 139.9,
                'price_yearly': 499.9,
                'description': '专业版功能 + 优先支持',
                'sort_order': 2
            }
        )
        self.stdout.write(self.style.SUCCESS(f'创建专业会员等级: {pro_tier.name}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\n会员等级初始化完成，共创建 {MembershipTier.objects.count()} 个等级'
            )
        ) 