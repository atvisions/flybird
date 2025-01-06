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

from membership.models import MembershipTier

def init_membership_tiers():
    """初始化会员等级"""
    print("\n=== 开始初始化会员等级 ===")
    
    # 删除现有等级
    MembershipTier.objects.all().delete()
    print("已清除现有会员等级")
    
    # 创建免费会员等级
    free_tier = MembershipTier.objects.create(
        name='免费用户',
        tier_type='free',
        price_monthly=0,
        price_quarterly=0,
        price_yearly=0,
        is_default=True,
        description='基础功能免费使用',
        sort_order=0
    )
    print(f"创建免费会员等级: {free_tier.name}")
    
    # 创建高级会员等级
    premium_tier = MembershipTier.objects.create(
        name='高级会员',
        tier_type='premium',
        price_monthly=29.9,
        price_quarterly=79.9,
        price_yearly=299.9,
        is_default=False,
        description='解锁全部高级功能',
        sort_order=1
    )
    print(f"创建高级会员等级: {premium_tier.name}")
    
    print("\n=== 会员等级初始化完成 ===")
    print(f"总计创建 {MembershipTier.objects.count()} 个会员等级")

if __name__ == '__main__':
    init_membership_tiers() 