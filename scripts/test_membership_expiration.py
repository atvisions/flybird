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
from membership.tasks import send_expiration_reminder, check_expired_memberships
import time

def test_membership_expiration():
    User = get_user_model()
    
    # 1. 获取或创建测试用户
    user, created = User.objects.get_or_create(
        phone='18818181898',
        defaults={
            'username': '测试用户',
            'email': 'liu.zhao@qq.com',  # 使用测试邮箱
            'is_active': True
        }
    )
    if created:
        user.set_password('123456')
        user.save()
        print("创建了新的测试用户")
    else:
        # 如果用户已存在，更新邮箱
        user.email = 'liu.zhao@qq.com'
        user.save(update_fields=['email'])
        print("更新了用户邮箱")
    
    print(f"\n1. 测试用户信息:")
    print(f"用户名: {user.username}")
    print(f"邮箱: {user.email}")
    
    # 2. 获取会员等级
    tier = MembershipTier.objects.filter(tier_type='premium').first()
    print(f"\n2. 会员等级信息:")
    print(f"等级名称: {tier.name}")
    print(f"等级类型: {tier.tier_type}")
    
    # 3. 创建即将到期的会员
    membership, created = UserMembership.objects.update_or_create(
        user=user,
        defaults={
            'tier': tier,
            'expire_time': localtime(timezone.now()) + timedelta(minutes=1)  # 使用本地时间
        }
    )
    print(f"\n3. 会员信息:")
    print(f"到期时间: {localtime(membership.expire_time)}")  # 显示本地时间
    print(f"是否新创建: {created}")
    
    # 4. 执行到期提醒任务
    print(f"\n4. 执行到期提醒任务:")
    print("检查日志文件...")
    os.system('tail -f logs/django.log &')  # 后台显示日志
    
    result = send_expiration_reminder.delay()
    print(f"任务ID: {result.id}")
    
    # 等待任务完成
    time.sleep(5)
    print(f"任务状态: {result.status}")
    print(f"任务结果: {result.get()}")
    
    # 停止日志显示
    os.system('pkill -f "tail -f logs/django.log"')
    
    # 5. 测试会员过期
    print(f"\n5. 测试会员过期:")
    # 设置为已过期
    membership.expire_time = localtime(timezone.now()) - timedelta(days=1)
    membership.save()
    print(f"设置过期时间为: {localtime(membership.expire_time)}")
    
    # 执行过期检查任务
    result = check_expired_memberships.delay()
    print(f"过期检查任务ID: {result.id}")
    
    # 等待任务完成
    time.sleep(5)
    
    # 验证会员状态
    membership.refresh_from_db()
    print(f"\n6. 验证最终状态:")
    print(f"当前会员等级: {membership.tier.name}")
    print(f"是否为默认等级: {membership.tier.is_default}")

if __name__ == '__main__':
    test_membership_expiration() 