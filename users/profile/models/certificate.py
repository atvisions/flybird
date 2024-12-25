from django.db import models
from django.conf import settings
from django.utils import timezone

class Certificate(models.Model):
    CERTIFICATE_TYPE_CHOICES = (
        ('professional', '专业证书'),
        ('award', '获奖证书'),
        ('language', '语言证书'),
        ('other', '其他证书')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name='用户'
    )
    name = models.CharField(max_length=100, verbose_name='证书名称')
    type = models.CharField(
        max_length=20,
        choices=CERTIFICATE_TYPE_CHOICES,
        default='professional',
        verbose_name='证书类型'
    )
    issuing_authority = models.CharField(max_length=100, verbose_name='发证机构')
    issue_date = models.DateField(verbose_name='发证日期')
    expiry_date = models.DateField(blank=True, null=True, verbose_name='到期日期')
    credential_id = models.CharField(max_length=100, blank=True, verbose_name='证书编号')
    description = models.TextField(blank=True, verbose_name='证书描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '证书奖项'
        verbose_name_plural = '证书奖项'
        ordering = ['-issue_date']

    def __str__(self):
        return f'{self.user.phone} 的证书: {self.name}' 