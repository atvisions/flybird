from django.db import models
from django.conf import settings
from django.utils import timezone
class JobIntention(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_intention',
        verbose_name='用户'
    )
    job_type = models.CharField(max_length=50, verbose_name='工作类型')
    expected_salary = models.CharField(max_length=50, verbose_name='期望薪资')
    expected_city = models.CharField(max_length=50, verbose_name='期望城市')
    job_status = models.CharField(max_length=50, verbose_name='求职状态')
    description = models.TextField(blank=True, verbose_name='求职说明')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '求职意向'
        verbose_name_plural = '求职意向'

    def __str__(self):
        return f'{self.user.phone} 的求职意向' 