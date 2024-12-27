from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from articles.models import Article
from qa.models import Answer
from .models import MembershipTier, UserMembership, UserPoint
from .services import PointService

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_membership(sender, instance, created, **kwargs):
    """创建用户时自动创建会员信息"""
    if created:
        # 创建会员信息
        default_tier = MembershipTier.objects.filter(is_default=True).first()
        UserMembership.objects.create(user=instance, tier=default_tier)
        
        # 创建积分账户
        UserPoint.objects.create(user=instance)

@receiver(post_save, sender=MembershipTier)
def handle_default_tier(sender, instance, **kwargs):
    """处理默认等级"""
    if instance.is_default:
        # 确保只有一个默认等级
        MembershipTier.objects.exclude(pk=instance.pk).update(is_default=False) 

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