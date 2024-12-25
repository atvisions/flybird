from django.db import models
from django.conf import settings
from django.utils import timezone
class Language(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='languages',
        verbose_name='用户'
    )
    name = models.CharField(max_length=50, verbose_name='语言名称')
    level = models.CharField(max_length=50, verbose_name='掌握程度')
    description = models.TextField(blank=True, verbose_name='语言描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '语言能力'
        verbose_name_plural = '语言能力'

    def __str__(self):
        return f'{self.user.phone} 的语言: {self.name}' 