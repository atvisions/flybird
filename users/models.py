from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
import time
from django.utils import timezone

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
    
    # 添加软删除字段
    is_deleted = models.BooleanField(
        _('已注销'), 
        default=False,
        help_text=_('用户是否已注销')
    )
    deleted_at = models.DateTimeField(
        _('注销时间'),
        null=True,
        blank=True
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
    
    # 添加新的字段
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='用户头像')
    background_image = models.ImageField(upload_to='backgrounds/', null=True, blank=True, verbose_name='背景图')
    position = models.CharField(max_length=100, null=True, blank=True, verbose_name='职位')
    bio = models.TextField(null=True, blank=True, verbose_name='个人简介')
    is_vip = models.BooleanField(default=False, verbose_name='是否是VIP用户')
    vip_expire_time = models.DateTimeField(null=True, blank=True, verbose_name='会员到期时间')
    vip_type = models.CharField(
        max_length=20, 
        choices=[
            ('none', '普通用户'),
            ('monthly', '月度会员'),
            ('yearly', '年度会员'),
            ('lifetime', '终身会员')
        ],
        default='none',
        verbose_name='会员类型'
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        if not self.pk:  # 如果是新用户
            # 先保存以获取 id
            super().save(*args, **kwargs)
            
            # 生成 uid (从10001开始)
            if not self.uid:
                # 获取当前最大的uid
                max_uid = User.objects.aggregate(Max('uid'))['uid__max']
                if max_uid:
                    # 如果存在用户，则在最大uid基础上+1
                    next_uid = int(max_uid) + 1
                else:
                    # 如果是第一个用户，从10001开始
                    next_uid = 10001
                self.uid = f"{next_uid}"
            
            # 设置默认用户名 - FB + uid + 时间戳后4位
            if not self.username:
                timestamp = str(int(time.time()))[-4:]  # 获取时间戳后4位
                self.username = f"FB{self.uid}{timestamp}"  # 例如: FB10001{timestamp}
                
            # 再次保存以更新 uid 和 username
            return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)

    @property
    def vip_status(self):
        """获取会员状态"""
        if not self.is_vip:
            return '普通用户'
        
        if self.vip_type == 'lifetime':
            return '终身会员'
            
        if not self.vip_expire_time:
            return '普通用户'
            
        now = timezone.now()
        if now > self.vip_expire_time:
            self.is_vip = False
            self.vip_type = 'none'
            self.save(update_fields=['is_vip', 'vip_type'])
            return '普通用户'
            
        days_left = (self.vip_expire_time - now).days
        return f"{self.get_vip_type_display()}（剩余{days_left}天）"

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
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

class VipOrder(models.Model):
    """会员订单"""
    ORDER_STATUS = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('cancelled', '已取消'),
        ('refunded', '已退款')
    ]
    
    VIP_TYPES = [
        ('monthly', '月度会员'),
        ('yearly', '年度会员'),
        ('lifetime', '终身会员')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vip_orders')
    order_no = models.CharField(max_length=64, unique=True, verbose_name='订单号')
    vip_type = models.CharField(max_length=20, choices=VIP_TYPES, verbose_name='会员类型')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    
    class Meta:
        verbose_name = '会员订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_vip_type_display()} - {self.get_status_display()}"


# ... 继续添加其他模型 ... 