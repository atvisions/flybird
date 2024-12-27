from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import UserMembership, MembershipOrder, MembershipTier
from .services import PaymentService
from django.core.mail import send_mail
from django.conf import settings
import logging
import traceback
from django.utils.timezone import localtime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .utils import get_logo_base64

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
    logger = logging.getLogger('membership')
    logger.info("开始执行会员到期提醒任务")
    
    now = localtime(timezone.now())
    
    # 获取7天内即将到期的会员
    expiring_soon = UserMembership.objects.filter(
        expire_time__range=(
            now,
            now + timedelta(days=7)
        )
    ).select_related('user', 'tier')
    
    logger.info(f"找到 {expiring_soon.count()} 个即将到期的会员")
    
    for membership in expiring_soon:
        logger.info(f"处理用户: {membership.user.username}, 邮箱: {membership.user.email}")
        if membership.user.email:
            days_left = (membership.expire_time - now).days
            logger.info(f"剩余天数: {days_left}")
            
            try:
                # 获取logo
                logo_base64 = get_logo_base64()
                
                # 渲染HTML模板
                context = {
                    'user': membership.user,
                    'membership': membership,
                    'days_left': days_left,
                    'logo_base64': logo_base64,
                    'renewal_url': settings.MEMBERSHIP_URLS['renewal']
                }
                html_message = render_to_string('email/expiration_reminder.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject='【飞鸟简历】会员即将到期提醒',
                    message=plain_message,
                    html_message=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[membership.user.email],
                    fail_silently=False
                )
                logger.info(f"邮件发送成功: {membership.user.email}")
            except Exception as e:
                logger.error(f"邮件发送失败: {str(e)}")
                logger.error(traceback.format_exc())
    
    return expiring_soon.count()

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