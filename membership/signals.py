from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from articles.models import Article
from qa.models import Answer
from .models import MembershipTier, UserMembership, UserPoint
from .services import PointService
from django.utils import timezone

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_membership(sender, instance, created, **kwargs):
    """创建用户时自动创建会员信息"""
    if created:
        # 创建会员信息
        default_tier = MembershipTier.get_default()
        if default_tier:
            UserMembership.objects.create(user=instance, tier=default_tier)
        
        # 创建积分账户
        UserPoint.objects.create(user=instance)

@receiver(post_save, sender=Article)
def handle_article_points(sender, instance, created, **kwargs):
    """处理文章积分"""
    if created:
        PointService.add_points(
            user=instance.author,
            event_type='publish_article',
            description=f'发布文章《{instance.title}》'
        )

@receiver(post_save, sender=Answer)
def handle_answer_points(sender, instance, created, **kwargs):
    """处理回答积分"""
    if created:
        PointService.add_points(
            user=instance.author,
            event_type='answer_question',
            description=f'回答问题《{instance.question.title}》'
        )
    elif instance.is_accepted and not instance._original_is_accepted:
        PointService.add_points(
            user=instance.author,
            event_type='best_answer',
            description=f'回答被采纳为最佳答案'
        ) 

@receiver(post_save, sender=UserMembership)
def sync_user_membership_status(sender, instance, **kwargs):
    """同步用户会员状态"""
    user = instance.user
    
    # 更新用户会员状态
    user.is_vip = instance.is_active
    user.vip_type = instance.tier.key if instance.is_active and instance.tier else 'none'
    user.vip_expire_time = instance.expire_time
    user.vip_status = instance.tier.name if instance.is_active and instance.tier else '普通用户'
    
    # 使用 update_fields 来只更新必要的字段
    user.save(update_fields=['is_vip', 'vip_type', 'vip_expire_time', 'vip_status']) 