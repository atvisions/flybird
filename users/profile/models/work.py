from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()

class WorkExperience(models.Model):
    """工作经历模型"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='work_experiences',
        verbose_name='用户'
    )
    company = models.CharField('公司名称', max_length=100)
    position = models.CharField('职位', max_length=100)
    department = models.CharField('部门', max_length=100, blank=True)
    start_date = models.DateField('入职时间')
    end_date = models.DateField('离职时间', null=True, blank=True)
    is_current = models.BooleanField('是否在职', default=False)
    description = models.TextField(
        '工作描述',
        validators=[MinLengthValidator(50)]
    )
    achievements = models.TextField('工作成就', blank=True)
    technologies = models.TextField('技术栈', blank=True)
    quality_score = models.FloatField('质量评分', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user_work_experience'
        verbose_name = '工作经历'
        verbose_name_plural = '工作经历'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.username} - {self.company} - {self.position}"

    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)

