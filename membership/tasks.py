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
from django.db.models import Q

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

logger = logging.getLogger('membership')

@shared_task
def check_membership_expiry():
    """检查会员到期情况并发送提醒"""
    from .models import UserMembership
    
    now = timezone.now()
    reminder_days = settings.MEMBERSHIP_EXPIRY_REMINDER['DAYS_BEFORE']
    
    logger.info(f"开始检查会员到期情况，当前时间: {now}")
    logger.info(f"邮件配置: backend={settings.EMAIL_BACKEND}")
    logger.info(f"发件人: {settings.DEFAULT_FROM_EMAIL}")
    
    for days in reminder_days:
        # 计算目标日期范围（当天的起始和结束时间）
        target_date = now + timezone.timedelta(days=days)
        start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # 查找即将到期的会员
        expiring_memberships = UserMembership.objects.filter(
            Q(expire_time__gte=start_of_day) & Q(expire_time__lte=end_of_day),
            tier__tier_type='premium'  # 只提醒付费会员
        ).select_related('user', 'tier')
        
        logger.info(f"检查 {days} 天后到期的会员，找到 {expiring_memberships.count()} 个")
        
        for membership in expiring_memberships:
            try:
                # 准备邮件内容
                context = {
                    'user': membership.user,
                    'membership': membership,
                    'days_left': days,
                    'renewal_url': f"{settings.FRONTEND_URL}/membership/renewal"
                }
                
                # 渲染邮件模板
                html_content = render_to_string(
                    'membership/email/expiry_reminder.html',
                    context
                )
                
                # 发送邮件
                send_mail(
                    subject=f'您的{membership.tier.name}即将到期',
                    message='',  # 纯文本内容可以为空
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[membership.user.email],
                    html_message=html_content,
                    fail_silently=False  # 不要静默失败
                )
                
                logger.info(
                    f"发送到期提醒成功: "
                    f"用户={membership.user.phone}, "
                    f"邮箱={membership.user.email}, "
                    f"等级={membership.tier.name}, "
                    f"到期时间={membership.expire_time}"
                )
                
            except Exception as e:
                logger.error(
                    f"发送到期提醒失败: "
                    f"用户={membership.user.phone}, "
                    f"错误={str(e)}",
                    exc_info=True
                )

@shared_task
def handle_expired_memberships():
    """处理已过期会员"""
    from .models import UserMembership, MembershipTier
    
    logger.info("开始处理已过期会员")
    
    # 获取默认等级
    default_tier = MembershipTier.objects.filter(is_default=True).first()
    if not default_tier:
        logger.error("找不到默认会员等级")
        return
    
    # 查找已过期会员
    expired_memberships = UserMembership.objects.filter(
        expire_time__lt=timezone.now(),
        tier__tier_type='premium'  # 只处理付费会员
    ).select_related('user', 'tier')
    
    logger.info(f"找到 {expired_memberships.count()} 个已过期会员")
    
    for membership in expired_memberships:
        try:
            # 记录原等级
            old_tier = membership.tier
            
            # 降级为默认等级
            membership.tier = default_tier
            membership.expire_time = None
            membership.save()
            
            logger.info(
                f"会员降级成功: "
                f"用户={membership.user.phone}, "
                f"原等级={old_tier.name}, "
                f"新等级={default_tier.name}"
            )
            
            # 发送通知
            context = {
                'user': membership.user,
                'old_tier': old_tier,
                'renewal_url': f"{settings.FRONTEND_URL}/membership/renewal"
            }
            
            html_content = render_to_string(
                'membership/email/membership_expired.html',
                context
            )
            
            send_mail(
                subject='您的会员已到期',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[membership.user.email],
                html_message=html_content,
                fail_silently=False
            )
            
            logger.info(f"发送到期通知成功: 用户={membership.user.phone}")
            
        except Exception as e:
            logger.error(
                f"处理过期会员失败: "
                f"用户={membership.user.phone}, "
                f"错误={str(e)}",
                exc_info=True
            ) 