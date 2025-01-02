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
    # 添加 UID 字段
    uid = models.CharField(
        _('用户ID'),
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        help_text=_('系统生成的唯一标识符')
    )
    
    # 允许 username 为空
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        null=True,
        unique=True
    )
    
    # 手机号字段
    phone = models.CharField(_('手机号'), max_length=11, unique=True)
    
    # 确保 email 是唯一的
    email = models.EmailField(
        _('email address'),
        unique=True,
        null=True,
        blank=True
    )
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        if not self.pk:  # 如果是新用户
            # 先保存以获取 id
            super().save(*args, **kwargs)
            # 生成 uid (保证7位数字)
            if not self.uid:
                self.uid = f"{10000 + self.pk:07d}"  # 格式化为5位数字
            # 设置默认用户名
            if not self.username:
                self.username = f"Flybird{self.phone[-4:]}"  # 使用手机号后4位作为默认用户名
            # 再次保存以更新 uid 和 username
            return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users_user'  # 使用默认的表名
        ordering = ['-date_joined']  # 按注册时间倒序排序

class ProfileScore(models.Model):
    """档案评分"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_score')
    total_score = models.DecimalField('总分', max_digits=5, decimal_places=2, default=0)
    basic_dimension = models.DecimalField('基础维度', max_digits=5, decimal_places=2, default=0)
    experience_dimension = models.DecimalField('经验维度', max_digits=5, decimal_places=2, default=0)
    ability_dimension = models.DecimalField('能力维度', max_digits=5, decimal_places=2, default=0)
    achievement_dimension = models.DecimalField('成就维度', max_digits=5, decimal_places=2, default=0)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '档案评分'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username} - {self.total_score}分"

# ... 继续添加其他模型 ... 