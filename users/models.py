from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('手机号不能为空')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', phone)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)

class User(AbstractUser):
    # 允许 username 为空
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        null=True,
        unique=True
    )
    
    # 只保留手机号字段
    phone = models.CharField(_('手机号'), max_length=11, unique=True)
    
    # 使用手机号登录
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'users_user'
        verbose_name = _('用户')
        verbose_name_plural = _('用户')
        
    def __str__(self):
        return self.phone 