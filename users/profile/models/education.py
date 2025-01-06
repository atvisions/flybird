from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Education(models.Model):
    """教育经历模型"""
    DEGREE_CHOICES = [
        ('high_school', '高中'),
        ('junior_college', '大专'),
        ('bachelor', '本科'),
        ('master', '硕士'),
        ('doctor', '博士'),
        ('other', '其他'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='educations',
        verbose_name='用户'
    )
    school = models.CharField('学校名称', max_length=100)
    major = models.CharField('专业', max_length=100)
    degree = models.CharField(
        '学历',
        max_length=20, 
        choices=DEGREE_CHOICES
    )
    start_date = models.DateField('入学时间')
    end_date = models.DateField('毕业时间', null=True, blank=True)
    is_current = models.BooleanField('是否在读', default=False)
    description = models.TextField('在校经历', blank=True)
    achievements = models.TextField('在校成就', blank=True)
    quality_score = models.FloatField('质量评分', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user_education'
        verbose_name = '教育经历'
        verbose_name_plural = '教育经历'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.username} - {self.school} - {self.major}"

    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)
