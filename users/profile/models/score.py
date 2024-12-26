from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class ProfileScore(models.Model):
    """用户档案评分"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_score'
    )
    
    basic_dimension = models.IntegerField(default=0)
    experience_dimension = models.IntegerField(default=0)
    ability_dimension = models.IntegerField(default=0)
    achievement_dimension = models.IntegerField(default=0)
    content_quality = models.FloatField(default=0)
    optimized_fields = models.JSONField(
        default=list,
        null=True,
        blank=True,
        help_text='记录已优化的字段'
    )

    class Meta:
        verbose_name = '档案评分'
        verbose_name_plural = '档案评分'
        db_table = 'users_profile_score'

    def __str__(self):
        return f'{self.user.phone} 的档案评分'
        
    @property
    def total_score(self):
        """计算总分"""
        base_score = (
            self.basic_dimension * 0.4 +
            self.experience_dimension * 0.3 +
            self.ability_dimension * 0.2 +
            self.achievement_dimension * 0.1
        )
        
        # 如果有内容质量分数，增加额外加分
        quality_bonus = 0
        if self.content_quality >= 8:  # 优秀
            quality_bonus = 5
        elif self.content_quality >= 6:  # 良好
            quality_bonus = 3
        elif self.content_quality > 0:  # 及格
            quality_bonus = 1
            
        return base_score + quality_bonus 