from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import User

class BasicInfo(models.Model):
    """基本信息"""
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    ]

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='basic_info'
    )
    name = models.CharField(_('姓名'), max_length=50, blank=True)
    avatar = models.ImageField(_('头像'), upload_to='avatars/', null=True, blank=True)
    gender = models.CharField(_('性别'), max_length=10, choices=GENDER_CHOICES, default='other')
    birthday = models.DateField(_('生日'), null=True, blank=True)
    location = models.CharField(_('所在地'), max_length=100, blank=True)
    email = models.EmailField(_('邮箱'), max_length=254, blank=True)
    job_title = models.CharField(_('职位'), max_length=100, null=True, blank=True)
    years_of_experience = models.IntegerField(_('工作年限'), null=True, blank=True)
    personal_summary = models.TextField(_('个人简介'), blank=True)

    class Meta:
        verbose_name = _('基本信息')
        verbose_name_plural = _('基本信息')
        db_table = 'user_basic_info'

    def __str__(self):
        return f"{self.user.phone} - {self.name}"

