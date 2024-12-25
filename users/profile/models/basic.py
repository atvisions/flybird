from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

class BasicInfo(models.Model):
    """基本信息"""
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
        ('other', '其他')
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basic_info', verbose_name='用户')
    name = models.CharField(max_length=50, verbose_name='姓名')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other', verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    location = models.CharField(max_length=100, blank=True, verbose_name='所在地')
    job_title = models.CharField(_('当前职位'), max_length=50, null=True, blank=True, help_text='例如：产品经理、前端工程师')
    bio = models.TextField(_('个人简介'), max_length=500, null=True, blank=True)
    email = models.EmailField(blank=True, verbose_name='邮箱')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user_basic_info'
        verbose_name = _('基本信息')
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name or '未设置姓名'}"

