from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import sys

class Command(BaseCommand):
    help = '测试邮件发送'

    def handle(self, *args, **kwargs):
        self.stdout.write("开始测试邮件发送...")
        self.stdout.write(f"使用的邮件后端: {settings.EMAIL_BACKEND}")
        
        try:
            # 直接打印到标准输出
            sys.stdout.write("\n准备发送邮件...\n")
            
            # 发送测试邮件
            result = send_mail(
                '测试邮件标题',
                '这是一封测试邮件内容',
                'service@popo.work',
                ['liu.zhao@qq.com'],
                fail_silently=False,
            )
            
            sys.stdout.write(f"\n邮件发送结果: {result}\n")
            self.stdout.write(self.style.SUCCESS('邮件发送完成'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'发送失败: {str(e)}'))
            sys.stdout.write(f"\n错误详情: {str(e)}\n") 