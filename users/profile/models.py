from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class ProfileLayout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_layout', verbose_name='用户')
    sections = models.JSONField(verbose_name='布局配置', default=list)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '档案布局'
        verbose_name_plural = '档案布局' 