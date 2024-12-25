from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.utils import timezone

class SocialLink(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='social_links',
        verbose_name=_('用户')
    )
    platform = models.CharField(_('平台名称'), max_length=50)
    url = models.URLField(_('链接地址'))
    description = models.TextField(_('链接描述'), blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '社交主页'
        verbose_name_plural = '社交主页'
        ordering = ['id']

    def __str__(self):
        return f'{self.platform} - {self.url}'
