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
    name = models.CharField('姓名', max_length=50, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True)
    background = models.ImageField('背景图', upload_to='backgrounds/', blank=True)
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField('出生日期', null=True, blank=True, default=None)
    phone = models.CharField('手机号', max_length=11, blank=True)
    email = models.EmailField('邮箱', blank=True)
    location = models.CharField('所在地', max_length=100, blank=True)
    personal_summary = models.TextField('个人简介', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.phone} - {self.name}"

    @property
    def avatar_url(self):
        """获取头像URL"""
        if self.avatar:
            return self.avatar.url
        return None

    @property
    def background_url(self):
        """获取背景图URL"""
        if self.background:
            return self.background.url
        return None

