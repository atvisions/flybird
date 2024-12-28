from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger('membership')

class Command(BaseCommand):
    help = '测试邮件发送'

    def handle(self, *args, **kwargs):
        try:
            # 打印配置
            self.stdout.write(f"DEBUG = {settings.DEBUG}")
            self.stdout.write(f"EMAIL_BACKEND = {settings.EMAIL_BACKEND}")
            self.stdout.write(f"DEFAULT_FROM_EMAIL = {settings.DEFAULT_FROM_EMAIL}")
            
            # 发送简单邮件
            result = send_mail(
                subject='简单测试邮件',
                message='这是一封测试邮件',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['liu.zhao@qq.com'],
                fail_silently=False,
            )
            
            self.stdout.write(self.style.SUCCESS(f'邮件发送结果: {result}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'邮件发送失败: {str(e)}'))
            logger.error('邮件发送失败', exc_info=True) 