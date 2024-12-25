from django.db import models
from django.conf import settings
from django.utils import timezone
class Education(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='educations',
        verbose_name='用户'
    )
    school = models.CharField(max_length=100, verbose_name='学校')
    major = models.CharField(max_length=100, verbose_name='专业')
    degree = models.CharField(max_length=50, verbose_name='学历')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期')
    is_current = models.BooleanField(default=False, verbose_name='是否在读')
    description = models.TextField(blank=True, verbose_name='教育经历描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '教育经历'
        verbose_name_plural = '教育经历'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.user.phone} 在 {self.school} 的教育经历'

    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)
