from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Language(models.Model):
    """语言能力模型"""
    PROFICIENCY_CHOICES = [
        ('elementary', '入门'),
        ('intermediate', '中级'),
        ('advanced', '高级'),
        ('native', '母语'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='languages',
        verbose_name='用户'
    )
    name = models.CharField('语言名称', max_length=50)
    proficiency = models.CharField(
        '熟练程度',
        max_length=20, 
        choices=PROFICIENCY_CHOICES,
        default='elementary',
        db_index=True
    )
    certification = models.CharField('语言证书', max_length=100, blank=True)
    score = models.CharField('考试分数', max_length=50, blank=True)
    quality_score = models.FloatField('质量评分', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user_language'
        verbose_name = '语言能力'
        verbose_name_plural = '语言能力'
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    @property
    def display_score(self):
        """显示分数"""
        if self.proficiency == 'native':
            return '母语'
        return f"{self.score}" if self.score else self.get_proficiency_display() 