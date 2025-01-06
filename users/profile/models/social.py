from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.utils import timezone

class SocialLink(models.Model):
    PLATFORM_CHOICES = [  # 使用列表而不是元组
        ('weibo', '新浪微博'),
        ('zhihu', '知乎'),
        ('zcool', '站酷'),
        ('douyin', '抖音'),
        ('bilibili', 'Bilibili'),
        ('github', 'GitHub'),
        ('twitter', 'Twitter'),
        ('website', '个人网站'),
        ('other', '其他')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='social_links',
        verbose_name=_('用户')
    )
    platform = models.CharField(
        _('平台名称'), 
        max_length=50,
        choices=PLATFORM_CHOICES
    )
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

    def get_platform_display(self):
        """手动实现获取平台显示名称的方法"""
        return dict(self.PLATFORM_CHOICES).get(self.platform, self.platform)