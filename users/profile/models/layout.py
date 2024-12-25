from django.db import models
from django.conf import settings
from django.utils import timezone

class ProfileLayout(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_layout',
        verbose_name='用户'
    )
    layout = models.JSONField(default=dict, verbose_name='布局配置')
    
    # 添加评分相关字段
    basic_dimension = models.IntegerField(default=0, verbose_name='基础维度分数')
    experience_dimension = models.IntegerField(default=0, verbose_name='经验维度分数')
    ability_dimension = models.IntegerField(default=0, verbose_name='能力维度分数')
    achievement_dimension = models.IntegerField(default=0, verbose_name='成就维度分数')
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '档案布局'
        verbose_name_plural = '档案布局'

    def __str__(self):
        return f'{self.user.phone} 的档案布局'
        
    @property
    def total_score(self):
        """计算总分"""
        return (
            self.basic_dimension * 0.4 +
            self.experience_dimension * 0.3 +
            self.ability_dimension * 0.2 +
            self.achievement_dimension * 0.1
        ) 