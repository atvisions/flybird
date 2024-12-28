from django.db import models
from django.utils import timezone
from users.models import User

class WorkExperience(models.Model):
    """工作经历"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='work_experiences',
        verbose_name='用户'
    )
    company = models.CharField('公司名称', max_length=100)
    position = models.CharField('职位', max_length=100)
    department = models.CharField('部门', max_length=100, blank=True)
    start_date = models.DateField('开始时间')
    end_date = models.DateField('结束时间', null=True, blank=True)
    is_current = models.BooleanField('是否当前工作', default=False)
    company_description = models.TextField('公司描述', blank=True)
    technologies = models.TextField('技术栈', blank=True)
    responsibilities = models.TextField('工作职责', blank=True)
    achievements = models.TextField('工作成果', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '工作经历'
        verbose_name_plural = verbose_name
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.username} - {self.company} - {self.position}"

    def save(self, *args, **kwargs):
        # 如果是当前工作，结束时间设为空
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)

