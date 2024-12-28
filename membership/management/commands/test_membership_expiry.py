from django.core.management.base import BaseCommand
from django.utils import timezone
from membership.models import UserMembership, MembershipTier
from users.models import User
from django.db import transaction
import logging

logger = logging.getLogger('membership')

class Command(BaseCommand):
    help = '测试会员到期提醒功能'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # 创建测试用户
                user, _ = User.objects.get_or_create(
                    phone='13800138000',
                    defaults={
                        'email': 'liu.zhao@qq.com',
                        'name': '测试用户',
                        'username': '测试用户'  # 添加用户名
                    }
                )
                
                # 获取或创建高级会员等级
                premium_tier, _ = MembershipTier.objects.get_or_create(
                    tier_type='premium',
                    defaults={
                        'name': '高级会员',
                        'price_monthly': 39.9,
                        'price_quarterly': 99.9,
                        'price_yearly': 399.9,
                        'description': '解锁全部高级功能',
                        'sort_order': 1
                    }
                )
                
                self.stdout.write(self.style.SUCCESS(f'会员等级: {premium_tier.name}'))
                
                # 创建不同到期时间的会员
                test_cases = [
                    (1, '1天后到期'),
                    (3, '3天后到期'),
                    (7, '7天后到期'),
                    (-1, '已过期1天'),
                    (-3, '已过期3天')
                ]
                
                for days, desc in test_cases:
                    expire_time = timezone.now() + timezone.timedelta(days=days)
                    membership, _ = UserMembership.objects.update_or_create(
                        user=user,
                        defaults={
                            'tier': premium_tier,
                            'expire_time': expire_time
                        }
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'创建测试会员成功: {desc}, '
                            f'用户={user.phone}, '
                            f'到期时间={expire_time}'
                        )
                    )
                    
                    # 测试到期提醒
                    from membership.tasks import check_membership_expiry, handle_expired_memberships
                    result = check_membership_expiry.delay()
                    self.stdout.write(self.style.SUCCESS(f'发送到期提醒任务: {result.id}'))
                    
                    result = handle_expired_memberships.delay()
                    self.stdout.write(self.style.SUCCESS(f'处理过期会员任务: {result.id}'))
                    
                    # 等待任务完成
                    result.get(timeout=10)
                    
                # 检查会员状态
                membership.refresh_from_db()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n当前会员状态:\n'
                        f'用户: {membership.user.phone}\n'
                        f'等级: {membership.tier.name}\n'
                        f'到期时间: {membership.expire_time}\n'
                        f'是否过期: {membership.is_expired}'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'测试失败: {str(e)}')
            )
            logger.error(f'测试失败: {str(e)}', exc_info=True) 