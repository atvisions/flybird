from django.db import models
from django.conf import settings
from django.utils import timezone
class Skill(models.Model):
    LEVEL_CHOICES = [
        ('初级', '初级'),
        ('中级', '中级'),
        ('高级', '高级'),
        ('专家', '专家')
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name='用户'
    )
    name = models.CharField('技能名称', max_length=50)
    level = models.CharField(
        '熟练程度',
        max_length=20,
        choices=LEVEL_CHOICES,
        default='初级',
        null=True,
        blank=True
    )
    description = models.TextField('技能描述', blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    projects = models.TextField('相关项目', blank=True)
    order = models.IntegerField(default=0, verbose_name='排序')
    class Meta:
        verbose_name = '技能'
        verbose_name_plural = verbose_name
        ordering = ['order']

    def __str__(self):
        return f'{self.user.username} 的技能: {self.name}'
