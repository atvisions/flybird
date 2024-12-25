from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import User
from users.profile.models.basic import BasicInfo
from users.profile.models.intention import JobIntention
from users.profile.models.layout import ProfileLayout

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    当创建新用户时自动创建完整的档案结构
    包括：基本信息、求职意向、档案布局等
    """
    if created:
        # 创建基本信息
        BasicInfo.objects.create(user=instance)
        
        # 创建求职意向
        JobIntention.objects.create(user=instance)
        
        # 创建档案布局
        ProfileLayout.objects.create(
            user=instance,
            layout={  # 使用 layout 而不是 sections
                'basic_info': {'order': 1, 'visible': True},
                'job_intention': {'order': 2, 'visible': True},
                'work_experience': {'order': 3, 'visible': True},
                'education': {'order': 4, 'visible': True},
                'project': {'order': 5, 'visible': True},
                'skill': {'order': 6, 'visible': True},
                'certificate': {'order': 7, 'visible': True},
                'language': {'order': 8, 'visible': True},
                'portfolio': {'order': 9, 'visible': True},
                'social_link': {'order': 10, 'visible': True}
            }
        )

@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """
    当删除用户时，关联的档案记录会通过 CASCADE 自动删除
    这个信号处理器用于处理可能的清理工作
    """
    try:
        # 删除头像文件
        if hasattr(instance, 'basic_info') and instance.basic_info.avatar:
            instance.basic_info.avatar.delete(save=False)
        
        # 删除作品集中的文件
        if hasattr(instance, 'portfolios'):
            portfolios = instance.portfolios.all()
            for portfolio in portfolios:
                if portfolio.image:
                    portfolio.image.delete(save=False)
    except Exception as e:
        # 记录错误但不影响删除过程
        print(f"Error cleaning up user files: {e}") 