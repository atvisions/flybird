import os
import django
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# 导入所需模块
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import timedelta
from membership.models import UserMembership, MembershipTier
from django.contrib.auth import get_user_model
from membership.tasks import send_expiration_reminder

def test_membership_reminder():
    User = get_user_model()
    
    print("\n=== 测试会员到期提醒 ===")
    
    # 1. 准备测试用户
    user = User.objects.get(phone='18818181898')
    user.email = 'liu.zhao@qq.com'
    user.save()
    print(f"\n当前用户信息:")
    print(f"用户名: {user.username}")
    print(f"邮箱: {user.email}")
    
    # 2. 设置会员即将到期
    tier = MembershipTier.objects.filter(tier_type='premium').first()
    expire_time = localtime(timezone.now()) + timedelta(days=6)  # 6天后到期
    
    membership, _ = UserMembership.objects.update_or_create(
        user=user,
        defaults={
            'tier': tier,
            'expire_time': expire_time
        }
    )
    
    print(f"\n会员信息:")
    print(f"等级: {membership.tier.name}")
    print(f"到期时间: {localtime(membership.expire_time)}")
    
    # 3. 执行到期提醒任务
    print(f"\n执行到期提醒任务...")
    result = send_expiration_reminder()
    print(f"处理的会员数量: {result}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_membership_reminder() 