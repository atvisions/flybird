from django.db import models
from django.conf import settings

class Language(models.Model):
    """语言能力"""
    PROFICIENCY_CHOICES = [
        ('elementary', '入门'),
        ('intermediate', '中级'),
        ('advanced', '高级'),
        ('proficient', '精通'),
        ('native', '母语'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='languages',
        verbose_name='用户'
    )
    name = models.CharField('语言名称', max_length=50)
    level = models.CharField(
        '掌握程度',
        max_length=20,
        choices=PROFICIENCY_CHOICES,
        default='intermediate'
    )
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '语言能力'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return f'{self.user.phone} 的语言: {self.name}' 