from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from django.db import transaction
import random
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class MembershipTier(models.Model):
    """会员等级"""
    TIER_CHOICES = [
        ('free', '免费用户'),
        ('basic', '基础会员'),
        ('pro', '高级会员'),
        ('premium', '超级会员')
    ]
    
    name = models.CharField('等级名称', max_length=50)
    key = models.CharField('等级标识', max_length=20, choices=TIER_CHOICES, default='free', unique=True)
    description = models.TextField('等级描述', blank=True)
    price_monthly = models.DecimalField('月度价格', max_digits=10, decimal_places=2)
    price_quarterly = models.DecimalField('季度价格', max_digits=10, decimal_places=2)
    price_yearly = models.DecimalField('年度价格', max_digits=10, decimal_places=2)
    sort_order = models.IntegerField('排序', default=0)
    status = models.BooleanField('是否启用', default=True)
    is_default = models.BooleanField('是否默认', default=False)
    benefits = models.JSONField('权益配置', default=dict)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '会员等级'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            # 确保只有一个默认等级
            type(self).objects.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_default(cls):
        """获取默认等级"""
        return cls.objects.filter(is_default=True, status=True).first()

class Privilege(models.Model):
    """权益项目"""
    name = models.CharField('权益名称', max_length=100)
    key = models.CharField('权益标识', max_length=50, unique=True)
    description = models.TextField('权益描述', blank=True)
    value_type = models.CharField('值类型', max_length=20, choices=[
        ('boolean', '是否类型'),
        ('number', '数值类型'),
        ('text', '文本类型')
    ])
    is_active = models.BooleanField('是否启用', default=True)
    sort_order = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = '权益项目'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.name

class TierPrivilege(models.Model):
    """等级权益配置"""
    tier = models.ForeignKey(MembershipTier, on_delete=models.CASCADE, related_name='privileges')
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE)
    value = models.JSONField('权益值')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '等级权益'
        verbose_name_plural = verbose_name
        unique_together = ['tier', 'privilege']

    def __str__(self):
        return f"{self.tier.name}-{self.privilege.name}"

class UserMembership(models.Model):
    """用户会员"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='membership'
    )
    tier = models.ForeignKey(
        MembershipTier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    expire_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def extend_membership(self, days):
        """延长会员时间"""
        now = timezone.now()
        if not self.expire_time or self.expire_time < now:
            self.expire_time = now + timezone.timedelta(days=days)
        else:
            self.expire_time = self.expire_time + timezone.timedelta(days=days)
        self.save()
        
        # 清除会员信息缓存
        from .services import MembershipCacheService
        MembershipCacheService.clear_user_membership_cache(self.user)

    @property
    def is_active(self):
        """会员是否有效"""
        if not self.expire_time:
            return False
        return self.expire_time > timezone.now()

    @property
    def remaining_days(self):
        """剩余天数"""
        if not self.expire_time:
            return 0
        now = timezone.now()
        if self.expire_time <= now:
            return 0
        delta = self.expire_time - now
        return delta.days

    def check_and_restore(self):
        """检查并恢复会员状态"""
        if not self.tier or not self.expire_time:
            return False
            
        # 如果已过期，检查是否有未处理的续费订单
        if self.expire_time < timezone.now():
            recent_order = MembershipOrder.objects.filter(
                user=self.user,
                status='paid',
                paid_time__gt=self.expire_time
            ).order_by('-paid_time').first()
            
            if recent_order:
                # 更新会员等级和到期时间
                self.tier = recent_order.tier
                self.extend_membership(recent_order.days)
                return True
                
        return False

    def __str__(self):
        return f"{self.user.username} - {self.tier.name if self.tier else '无会员'}"

    class Meta:
        verbose_name = '用户会员'
        verbose_name_plural = '用户会员'

class MembershipOrder(models.Model):
    """会员订单"""
    ORDER_STATUS = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_METHODS = [
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
    ]
    
    order_no = models.CharField('订单号', max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_orders')
    tier = models.ForeignKey(MembershipTier, on_delete=models.PROTECT)
    amount = models.DecimalField('金额', max_digits=10, decimal_places=2)
    days = models.IntegerField('天数')
    payment_method = models.CharField('支付方式', max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField('状态', max_length=20, choices=ORDER_STATUS, default='pending')
    paid_time = models.DateTimeField('支付时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '会员订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_no}-{self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = f"M{timezone.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)

    @transaction.atomic
    def complete_payment(self):
        """完成支付"""
        if self.status != 'pending':
            return False
        
        self.status = 'paid'
        self.paid_time = timezone.now()
        self.save()

        # 更新会员信息
        membership, created = UserMembership.objects.get_or_create(
            user=self.user,
            defaults={'tier': self.tier}
        )

        if not created:
            membership.tier = self.tier

        # 计算新的到期时间
        if membership.expire_time and membership.expire_time > timezone.now():
            membership.expire_time += timezone.timedelta(days=self.days)
        else:
            membership.expire_time = timezone.now() + timezone.timedelta(days=self.days)

        membership.status = True
        membership.save()

        return True

class PointRule(models.Model):
    """积分规则"""
    name = models.CharField('规则名称', max_length=100)
    event_type = models.CharField('事件类型', max_length=50, unique=True)
    points = models.IntegerField('积分值')
    is_active = models.BooleanField('是否启用', default=True)
    description = models.TextField('规则描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '积分规则'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class UserPoint(models.Model):
    """用户积分"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='point'
    )
    balance = models.IntegerField(default=0)
    total_earned = models.IntegerField(default=0)
    point_level = models.IntegerField(default=1)
    sign_in_days = models.IntegerField(default=0)
    last_sign_in = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_points'
        verbose_name = '用户积分'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username} - {self.balance}积分"

    def update_level(self):
        """更新积分等级"""
        if self.total_earned < 1000:
            self.point_level = 1
        elif self.total_earned < 5000:
            self.point_level = 2
        elif self.total_earned < 20000:
            self.point_level = 3
        elif self.total_earned < 50000:
            self.point_level = 4
        else:
            self.point_level = 5

class PointRecord(models.Model):
    """积分记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_records')
    rule = models.ForeignKey(PointRule, on_delete=models.SET_NULL, null=True)
    points = models.IntegerField('积分变动')
    balance = models.IntegerField('变动后余额')
    event_type = models.CharField('事件类型', max_length=50)
    description = models.CharField('描述', max_length=200)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '积分记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}-{self.points}" 