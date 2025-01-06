from django.db import models
from django.conf import settings
from django.utils import timezone

class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='用户'
    )
    name = models.CharField(max_length=100, verbose_name='项目名称')
    role = models.CharField(max_length=100, verbose_name='担任角色')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期')
    is_current = models.BooleanField(default=False, verbose_name='是否进行中')
    description = models.TextField(blank=True, verbose_name='项目描述')
    achievement = models.TextField(blank=True, verbose_name='项目成果')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '项目经历'
        verbose_name_plural = '项目经历'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.user.phone} 的项目: {self.name}'

    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs) 