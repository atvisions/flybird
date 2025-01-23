from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Resume(models.Model):
    """简历模型"""
    STATUS_CHOICES = (
        (0, _('草稿')),
        (1, _('已发布')),
    )

    # 基本信息
    name = models.CharField(_('简历名称'), max_length=100)
    description = models.TextField(_('简历描述'), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_('创建者'),
        on_delete=models.CASCADE,
        related_name='resumes'
    )
    template = models.ForeignKey(
        'template_editor.Template',
        verbose_name=_('使用的模板'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # 画布数据
    pages = models.JSONField(_('画布页面'), default=list, help_text=_('存储多个画布页面的数据'))
    status = models.SmallIntegerField(_('状态'), choices=STATUS_CHOICES, default=0)
    is_public = models.BooleanField(_('是否公开'), default=False)
    
    # 统计信息
    view_count = models.IntegerField(_('浏览次数'), default=0)
    download_count = models.IntegerField(_('下载次数'), default=0)
    
    # 时间信息
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('简历')
        verbose_name_plural = _('简历')
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
