from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

class JobIntention(models.Model):
    """求职意向"""
    JOB_TYPE_CHOICES = [
        ('full_time', '全职'),
        ('part_time', '兼职'),
        ('internship', '实习'),
        ('freelance', '自由职业'),
    ]
    
    JOB_STATUS_CHOICES = [
        ('open', '在找工作'),
        ('closed', '暂不找工作'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='job_intention'
    )
    job_type = models.CharField(_('工作类型'), max_length=20, choices=JOB_TYPE_CHOICES)
    expected_salary = models.CharField(_('期望薪资'), max_length=50)
    expected_city = models.CharField(_('期望城市'), max_length=50)
    job_status = models.CharField(_('求职状态'), max_length=20, choices=JOB_STATUS_CHOICES)
    industries = models.CharField(
        _('期望行业'), 
        max_length=200,
        blank=True,
        null=True,
        default=''
    )

    class Meta:
        verbose_name = _('求职意向')
        verbose_name_plural = _('求职意向')
        db_table = 'users_jobintention'

    def __str__(self):
        return f"{self.user.phone} - {self.get_job_type_display()}" 