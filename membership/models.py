from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
from django.conf import settings
from django.db import transaction
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class MembershipTier(models.Model):
    """会员等级"""
    name = models.CharField('等级名称', max_length=50)
    tier_type = models.CharField('等级类型', max_length=20, choices=[
        ('free', '免费用户'),
        ('premium', '付费会员')
    ])
    price_monthly = models.DecimalField('月付价格', max_digits=10, decimal_places=2)
    price_quarterly = models.DecimalField('季付价格', max_digits=10, decimal_places=2)
    price_yearly = models.DecimalField('年付价格', max_digits=10, decimal_places=2)
    is_default = models.BooleanField('是否默认等级', default=False)
    description = models.TextField('等级描述', blank=True)
    sort_order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '会员等级'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.name

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
    """用户会员信息"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='membership'
    )
    tier = models.ForeignKey(
        MembershipTier,
        on_delete=models.PROTECT,
        verbose_name='会员等级'
    )
    expire_time = models.DateTimeField('到期时间', null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '用户会员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.phone}-{self.tier.name}"
    
    def save(self, *args, **kwargs):
        # 如果没有设置等级，使用默认等级
        if not self.tier_id:
            default_tier = MembershipTier.objects.filter(
                models.Q(is_default=True) | models.Q(tier_type='free')
            ).first()
            if default_tier:
                self.tier = default_tier
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        """是否已过期"""
        if not self.expire_time:
            return True
        return self.expire_time < timezone.now()
    
    @property
    def remaining_days(self):
        """剩余天数"""
        if not self.expire_time:
            return 0
        if self.is_expired:
            return 0
        delta = self.expire_time - timezone.now()
        return max(0, delta.days)
    
    def extend_membership(self, days):
        """延长会员时间"""
        now = timezone.now()
        if not self.expire_time or self.expire_time < now:
            # 如果没有到期时间或已过期，从当前时间开始计算
            self.expire_time = now + timezone.timedelta(days=days)
        else:
            # 如果未过期，在当前到期时间基础上延长
            self.expire_time += timezone.timedelta(days=days)
        self.save()
        
    def check_and_restore(self):
        """检查并恢复会员状态"""
        # 如果有未支付的订单，检查是否已支付
        pending_orders = MembershipOrder.objects.filter(
            user=self.user,
            status='pending',
            created_at__gte=timezone.now() - timezone.timedelta(days=7)  # 只检查7天内的订单
        ).order_by('-created_at')
        
        for order in pending_orders:
            try:
                # 调用支付宝查询接口
                payment_service = PaymentService()
                trade_status = payment_service.query_order(order)
                
                if trade_status in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
                    # 订单已支付但状态未更新，进行恢复
                    with transaction.atomic():
                        order.status = 'paid'
                        order.paid_time = timezone.now()
                        order.save()
                        
                        self.tier = order.tier
                        self.extend_membership(order.days)
                        
                    logger.info(f"恢复会员状态成功: 用户={self.user.phone}, 订单={order.order_no}")
                    return True
                    
            except Exception as e:
                logger.error(f"检查订单状态失败: {str(e)}")
                continue
                
        return False

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
    
    def save(self, *args, **kwargs):
        # 生成订单号
        if not self.order_no:
            self.order_no = f"O{timezone.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='points')
    balance = models.IntegerField('积分余额', default=0)
    total_earned = models.IntegerField('总获得积分', default=0)
    total_spent = models.IntegerField('总消费积分', default=0)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户积分'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}-{self.balance}积分"

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