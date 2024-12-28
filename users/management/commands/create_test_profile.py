from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from users.models import User
from users.profile.models import (
    BasicInfo, WorkExperience, Education, 
    Skill, Certificate, Language, Portfolio
)
from time import sleep

class Command(BaseCommand):
    help = '创建测试用户和档案数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='清除已存在的测试数据',
        )

    def handle(self, *args, **options):
        phone = '13800138000'
        user_id = 3  # 固定用户ID
        
        try:
            with transaction.atomic():
                # 先删除所有关联数据
                user = User.objects.filter(phone=phone).first()
                if user:
                    self.stdout.write(f'开始清理用户数据: {phone}')
                    BasicInfo.objects.filter(user=user).delete()
                    WorkExperience.objects.filter(user=user).delete()
                    Education.objects.filter(user=user).delete()
                    Skill.objects.filter(user=user).delete()
                    Certificate.objects.filter(user=user).delete()
                    Language.objects.filter(user=user).delete()
                    Portfolio.objects.filter(user=user).delete()
                    user.delete()
                    self.stdout.write(self.style.SUCCESS(f'成功清理用户数据: {phone}'))
        
            # 创建新用户，禁用信号
            from django.db.models.signals import post_save
            from users.signals import create_user_profile
            
            # 临时断开信号
            post_save.disconnect(create_user_profile, sender=User)
            
            # 创建用户
            user = User.objects.create(
                id=user_id,
                phone=phone,
                username='test_user',
                is_active=True,
                uid=f'1{user_id:04d}'  # 手动设置 uid
            )
            user.set_password('password123')
            user.save()
            
            # 重新连接信号
            post_save.connect(create_user_profile, sender=User)
            
            self.stdout.write(self.style.SUCCESS(f'创建测试用户: {phone}, ID: {user_id}, UID: {user.uid}'))
            
            # 手动创建基本信息
            basic_info = BasicInfo.objects.create(
                user=user,
                name='张三',
                gender='male',
                personal_summary='5年Python开发经验，专注于后端系统开发和架构设计。熟悉Django框架，具有大型项目开发经验。',
                birth_date=timezone.now().date() - timezone.timedelta(days=365*28),
                phone=phone,
                email='zhangsan@example.com',
                location='上海市浦东新区'  # 添加所在地
            )
            self.stdout.write(self.style.SUCCESS(f'创建基本信息: {basic_info.name}'))
            
            # 创建或更新工作经历
            work_exp, _ = WorkExperience.objects.update_or_create(
                user=user,
                company='某科技公司',
                position='高级Python开发工程师',
                defaults={
                    'start_date': timezone.now().date() - timezone.timedelta(days=365*2),
                    'is_current': True,
                    'department': '技术研发部',
                    'responsibilities': '''
                    1. 负责公司核心业务系统的后端开发和维护
                    2. 参与系统架构设计和技术方案制定
                    3. 带领团队完成重点项目的开发工作
                    4. 进行代码审查和技术指导
                    '''.strip(),
                    'achievements': '''
                    1. 优化系统性能，将接口响应时间降低50%
                    2. 重构核心模块，提升代码质量和可维护性
                    3. 设计并实现自动化部署流程，缩短发布时间80%
                    4. 指导团队成员，提升团队整体技术水平
                    '''.strip(),
                    'company_description': '一家专注于企业��务的互联网科技公司，拥有自主研发的SaaS平台',
                    'technologies': 'Python, Django, MySQL, Redis, Docker, Kubernetes'
                }
            )
            
            # 创建教育经历
            edu, _ = Education.objects.get_or_create(
                user=user,
                school='某大学',
                major='计算机科学与技术',
                defaults={
                    'degree': '本科',
                    'start_date': timezone.now().date() - timezone.timedelta(days=365*6),
                    'end_date': timezone.now().date() - timezone.timedelta(days=365*2),
                    'description': '''
                    主修计算机科学与技术专业
                    主要课程：数据结构、算法分析、操作系统、计算机网络、数据库系统
                    在校成绩优异，获得校级奖学金
                    参与多个实验室项目，积累了丰富的实践经验
                    '''.strip(),
                    'is_current': False
                }
            )
            self.stdout.write(self.style.SUCCESS(f'创建教育经历: {edu.school}'))
            
            # 创建技能
            skill, _ = Skill.objects.get_or_create(
                user=user,
                name='Python开发',
                defaults={
                    'level': '熟练',
                    'description': '''
                    熟练掌握 Python 开发，精通 Django 框架
                    具有丰富的 Web 后端开发经验
                    熟悉常用的数据库、缓存、消息队列等中间件
                    有大型项目的架构设计和优化经验
                    '''.strip(),
                    'projects': '企业内部系统、电商平台、数据分析系统'
                }
            )
            self.stdout.write(self.style.SUCCESS(f'创建技能: {skill.name}'))
            
            # 创建证书
            cert, _ = Certificate.objects.get_or_create(
                user=user,
                name='Python高级工程师认证',
                defaults={
                    'issuing_authority': 'Python开发者协会',
                    'issue_date': timezone.now().date() - timezone.timedelta(days=365),
                    'description': '通过Python高级工程师认证考试'  # 简单的描述
                }
            )
            
            # 创建语言能力
            lang, _ = Language.objects.get_or_create(
                user=user,
                name='英语',
                defaults={
                    'level': 'CET-6',
                    'description': '可以流畅阅读英文技术文档，进行日常交流'  # 简单的描述
                }
            )
            
            # 创建作品集
            port, _ = Portfolio.objects.get_or_create(
                user=user,
                title='企业内部管理系统',
                defaults={
                    'description': '使用Django开发的企业内部系统',  # 简单的描述
                    'url': 'http://example.com',
                    'highlights': '实现了自动化办公流程'
                }
            )
            
            self.stdout.write(self.style.SUCCESS('成功创建测试用户和档案数据'))
            self.stdout.write(self.style.SUCCESS(f'用户名: {phone}'))
            self.stdout.write(self.style.SUCCESS('密码: password123'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'创建测试数据失败: {str(e)}')) 