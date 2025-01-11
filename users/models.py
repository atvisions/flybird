from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
import time
from django.utils import timezone

class CustomUserManager(UserManager):
    def _create_user(self, phone, password=None, **extra_fields):
        """
        创建用户的主要方法
        """
        if not phone:
            raise ValueError('手机号不能为空')
            
        # 生成用户名
        username = extra_fields.pop('username', None)
        if not username:
            # 生成临时用户名
            timestamp = str(int(time.time()))[-4:]
            username = f"FB{timestamp}{phone[-4:]}"
            
        user = self.model(phone=phone, username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)

class User(AbstractUser):
    """用户模型"""
    uid = models.CharField('用户ID', max_length=32, unique=True, null=True, blank=True)
    phone = models.CharField('手机号', max_length=11, unique=True)
    email = models.EmailField('邮箱', null=True, blank=True)
    avatar = models.URLField('头像', max_length=255, null=True, blank=True)
    background_image = models.URLField('背景图', max_length=255, null=True, blank=True)
    position = models.CharField('职位', max_length=50, null=True, blank=True)
    bio = models.TextField('简介', max_length=500, null=True, blank=True)
    
    # 会员相关字段
    is_vip = models.BooleanField('是否是会员', default=False, db_index=True)
    vip_type = models.CharField('会员类型', max_length=50, default='none', db_index=True)
    vip_expire_time = models.DateTimeField('会员过期时间', null=True, blank=True)
    vip_status = models.CharField('会员状态', max_length=50, default='普通用户')

    objects = CustomUserManager()  # 使用自定义的管理器

    USERNAME_FIELD = 'phone'  # 使用手机号作为主要标识符
    REQUIRED_FIELDS = []  # username 不再是必需字段

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'users_user'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username}({self.phone})"

    def save(self, *args, **kwargs):
        if not self.pk:  # 如果是新用户
            # 先保存以获取 id
            super().save(*args, **kwargs)
            
            # 生成 uid (从10001开始)
            if not self.uid:
                # 获取当前最大的uid
                max_uid = User.objects.aggregate(Max('uid'))['uid__max']
                if max_uid:
                    next_uid = int(max_uid) + 1
                else:
                    next_uid = 10001
                self.uid = f"{next_uid}"
            
            # 设置默认用户名 - FB + uid + 时间戳后4位
            if not self.username:
                timestamp = str(int(time.time()))[-4:]
                self.username = f"FB{self.uid}{timestamp}"
                
            # 再次保存以更新 uid 和 username
            return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)

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