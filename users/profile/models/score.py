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

    class Meta:
        verbose_name = '档案评分'
        verbose_name_plural = '档案评分'
        db_table = 'users_profile_score'

    def __str__(self):
        return f'{self.user.phone} 的档案评分'
        
    @property
    def total_score(self):
        """计算总分"""
        return (
            self.basic_dimension * 0.4 +
            self.experience_dimension * 0.3 +
            self.ability_dimension * 0.2 +
            self.achievement_dimension * 0.1
        ) 