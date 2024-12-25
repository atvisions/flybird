from django.db import models
from django.conf import settings
from django.utils import timezone

class Portfolio(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolios',
        verbose_name='用户'
    )
    title = models.CharField(max_length=100, verbose_name='作品标题')
    description = models.TextField(blank=True, verbose_name='作品描述')
    url = models.URLField(blank=True, verbose_name='作品链接')
    image = models.ImageField(upload_to='portfolios/', blank=True, verbose_name='作品图片')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '作品集'
        verbose_name_plural = '作品集'

    def __str__(self):
        return f'{self.user.phone} 的作品: {self.title}' 