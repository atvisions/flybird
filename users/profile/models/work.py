from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
class WorkExperience(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='work_experiences',
        verbose_name='用户'
    )
    company = models.CharField(max_length=100, verbose_name='公司名称')
    position = models.CharField(max_length=100, verbose_name='职位')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期')
    is_current = models.BooleanField(default=False, verbose_name='是否在职')
    is_internship = models.BooleanField(default=False, verbose_name='是否是实习')
    description = models.TextField(blank=True, verbose_name='工作描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '工作经历'
        verbose_name_plural = '工作经历'
        ordering = ['-start_date']  # 按开始日期倒序排列

    def __str__(self):
        return f'{self.user.phone} 在 {self.company} 的工作经历'

    def save(self, *args, **kwargs):
        # 如果是当前工作，结束日期设为空
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)

