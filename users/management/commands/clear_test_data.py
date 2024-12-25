from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = '清理测试数据'

    def handle(self, *args, **kwargs):
        test_phones = ['13800138000', '13900139000']
        
        with connection.cursor() as cursor:
            # 1. 获取用户IDs
            user_ids = list(User.objects.filter(phone__in=test_phones).values_list('id', flat=True))
            if not user_ids:
                self.stdout.write(self.style.SUCCESS('没有找到测试用户'))
                return
                
            # 2. 删除所有关联数据 (按照外键依赖顺序)
            tables = [
                'token_blacklist_blacklistedtoken',  # token 黑名单
                'token_blacklist_outstandingtoken',  # token
                'users_sociallink',         # 社交链接
                'users_portfolio',          # 作品集
                'users_language',           # 语言能力
                'users_certificate',        # 证书
                'users_skill',              # 技能
                'users_project',            # 项目经历
                'users_education',          # 教育经历
                'users_workexperience',     # 工作经历
                'users_jobintention',       # 求职意向
                'users_profile_score',      # 档案评分
                'users_profilelayout',      # 档案布局
                'user_basic_info',          # 基本信息
            ]
            
            for table in tables:
                try:
                    # 添加错误处理，如果表不存在则跳过
                    cursor.execute(
                        f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = %s",
                        [table]
                    )
                    if cursor.fetchone()[0] == 0:
                        self.stdout.write(self.style.WARNING(f'表 {table} 不存在，跳过'))
                        continue
                        
                    cursor.execute(f"DELETE FROM {table} WHERE user_id IN %s", [tuple(user_ids)])
                    rows = cursor.rowcount
                    self.stdout.write(f'从 {table} 删除了 {rows} 条记录')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'删除 {table} 数据时出错: {str(e)}'))
            
            # 3. 最后删除用户
            cursor.execute("DELETE FROM users_user WHERE id IN %s", [tuple(user_ids)])
            rows = cursor.rowcount
            self.stdout.write(f'删除了 {rows} 个用户')
        
        self.stdout.write(self.style.SUCCESS('测试数据清理完成')) 