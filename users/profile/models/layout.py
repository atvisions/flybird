from django.db import models
from django.conf import settings
from django.utils import timezone
class ProfileLayout(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_layout',
        verbose_name='用户'
    )
    layout = models.JSONField(default=dict, verbose_name='布局配置')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '档案布局'
        verbose_name_plural = '档案布局'

    def __str__(self):
        return f'{self.user.phone} 的档案布局' 