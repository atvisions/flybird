from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import UserMembership, MembershipOrder, MembershipTier
from .services import PaymentService

@shared_task
def process_payment_callback(order_id, payment_data):
    """处理支付回调"""
    try:
        order = MembershipOrder.objects.get(id=order_id)
        PaymentService.complete_order(order)
    except MembershipOrder.DoesNotExist:
        return False
    return True

@shared_task
def check_expired_memberships():
    """检查过期会员"""
    now = timezone.now()
    expired_memberships = UserMembership.objects.filter(
        expire_time__lt=now,
        tier__tier_type='premium'
    ).select_related('tier')
    
    # 获取默认等级
    default_tier = MembershipTier.objects.filter(is_default=True).first()
    if not default_tier:
        return False
    
    # 批量更新过期会员
    count = expired_memberships.update(
        tier=default_tier,
        updated_at=now
    )
    
    return count

@shared_task
def send_expiration_reminder():
    """发送会员到期提醒"""
    now = timezone.now()
    expiring_soon = UserMembership.objects.filter(
        expire_time__gt=now,
        expire_time__lt=now + timedelta(days=3),
        tier__tier_type='premium'
    ).select_related('user', 'tier')
    
    for membership in expiring_soon:
        try:
            # TODO: 接入消息通知系统
            # 可以发送短信、邮件或站内信
            pass
        except Exception as e:
            continue
    
    return len(expiring_soon)

@shared_task
def cancel_expired_orders():
    """取消过期订单"""
    expire_time = timezone.now() - timedelta(hours=24)  # 24小时未支付的订单自动取消
    expired_orders = MembershipOrder.objects.filter(
        status='pending',
        created_at__lt=expire_time
    )
    
    count = expired_orders.update(
        status='cancelled',
        updated_at=timezone.now()
    )
    
    return count 