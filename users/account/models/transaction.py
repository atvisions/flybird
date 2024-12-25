from django.db import models
from django.conf import settings
from django.utils import timezone

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('recharge', '充值'),
        ('consume', '消费'),
        ('refund', '退款'),
        ('withdraw', '提现'),
    )

    STATUS_CHOICES = (
        ('pending', '处理中'),
        ('success', '成功'),
        ('failed', '失败'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,  # 保护删除，不允许删除有交易记录的用户
        related_name='transactions',
        verbose_name='用户'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, verbose_name='交易类型')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    order_id = models.CharField(max_length=100, unique=True, verbose_name='订单号')
    description = models.CharField(max_length=200, blank=True, verbose_name='交易描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = '交易记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.phone} - {self.get_transaction_type_display()} - {self.amount}' 