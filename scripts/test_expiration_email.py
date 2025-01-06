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
import logging

logger = logging.getLogger('membership')

def test_expiration_email():
    """测试会员到期提醒邮件"""
    User = get_user_model()
    
    print("\n=== 开始测试会员到期提醒邮件 ===")
    
    # 1. 准备测试用户
    user, created = User.objects.get_or_create(
        phone='18818181898',
        defaults={
            'username': '测试用户',
            'email': 'liu.zhao@qq.com',
            'is_active': True
        }
    )
    if not created:
        user.email = 'liu.zhao@qq.com'
        user.save(update_fields=['email'])
    
    print(f"\n1. 测试用户信息:")
    print(f"用户名: {user.username}")
    print(f"邮箱: {user.email}")
    
    # 2. 准备会员等级
    tier = MembershipTier.objects.filter(tier_type='premium').first()
    if not tier:
        print("错误: 未找到高级会员等级")
        return
    
    print(f"\n2. 会员等级信息:")
    print(f"等级名称: {tier.name}")
    print(f"等级类型: {tier.tier_type}")
    
    # 3. 创建测试场景
    test_scenarios = [
        {'days': 1, 'desc': '明天到期'},
        {'days': 3, 'desc': '3天后到期'},
        {'days': 7, 'desc': '7天后到期'}
    ]
    
    for scenario in test_scenarios:
        print(f"\n=== 测试场景: {scenario['desc']} ===")
        
        # 设置到期时间
        expire_time = localtime(timezone.now()) + timedelta(days=scenario['days'])
        
        # 更新或创建会员
        membership, _ = UserMembership.objects.update_or_create(
            user=user,
            defaults={
                'tier': tier,
                'expire_time': expire_time
            }
        )
        
        print(f"到期时间: {localtime(membership.expire_time)}")
        
        # 执行提醒任务
        print("发送提醒邮件...")
        try:
            result = send_expiration_reminder()
            print(f"处理的会员数量: {result}")
            print("邮件发送成功!")
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")
        
        print("等待5秒后测试下一个场景...")
        import time
        time.sleep(5)
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_expiration_email() 