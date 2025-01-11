from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User

class Command(BaseCommand):
    help = '检查并更新用户的会员状态'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_users = User.objects.filter(
            is_vip=True,
            vip_type__in=['monthly', 'yearly'],
            vip_expire_time__lt=now
        )
        
        count = expired_users.count()
        expired_users.update(
            is_vip=False,
            vip_type='none'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {count} expired VIP users')
        ) 