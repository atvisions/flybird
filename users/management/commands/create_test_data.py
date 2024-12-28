from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.profile.models import (
    BasicInfo, JobIntention, WorkExperience, Education,
    Project, Skill, Certificate, Language, Portfolio, SocialLink
)

User = get_user_model()

class Command(BaseCommand):
    help = '创建测试数据'

    def handle(self, *args, **kwargs):
        # 创建测试用户
        user, created = User.objects.get_or_create(
            phone='13800138000',
            defaults={
                'username': 'test_user',
                'is_active': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('创建测试用户成功'))

        # 创建基本信息
        basic_info, _ = BasicInfo.objects.get_or_create(
            user=user,
            defaults={
                'name': '张三',
                'gender': 'male',
                'birth_date': '1995-01-01',
                'email': 'zhangsan@example.com',
                'location': '上海市',
                'personal_summary': '5年Python开发经验，专注于后端开发和系统架构设计。'
            }
        )
        self.stdout.write(self.style.SUCCESS('创建基本信息成功'))

        # 创建工作经历
        work_exp, _ = WorkExperience.objects.get_or_create(
            user=user,
            company='某科技公司',
            position='高级Python开发工程师',
            defaults={
                'start_date': '2020-01-01',
                'is_current': True,
                'department': '技术部',
                'company_description': '一家互联网科技公司',
                'responsibilities': '负责核心系统开发',
                'achievements': '优化系统性能提升50%',
                'technologies': 'Python, Django, MySQL'
            }
        )
        self.stdout.write(self.style.SUCCESS('创建工作经历成功'))

        # 创建教育经历
        education, _ = Education.objects.get_or_create(
            user=user,
            school='某大学',
            major='计算机科学与技术',
            defaults={
                'degree': '本科',
                'start_date': '2016-09-01',
                'end_date': '2020-07-01',
                'description': '主修计算机科学与技术'
            }
        )
        self.stdout.write(self.style.SUCCESS('创建教育经历成功'))

        # 创建技能
        skill, _ = Skill.objects.get_or_create(
            user=user,
            name='Python开发',
            defaults={
                'level': '精通',
                'description': '熟练掌握Python开发',
                'projects': '开发过多个大型项目'
            }
        )
        self.stdout.write(self.style.SUCCESS('创建技能成功'))

        # 创建证书
        certificate, _ = Certificate.objects.get_or_create(
            user=user,
            name='Python高级工程师认证',
            defaults={
                'type': 'professional',
                'issuing_authority': 'Python协会',
                'issue_date': '2022-01-01',
                'description': 'Python高级工程师认证'
            }
        )
        self.stdout.write(self.style.SUCCESS('创建证书成功'))

        # 创建语言能力
        language, _ = Language.objects.get_or_create(
            user=user,
            name='英语',
            defaults={
                'level': 'advanced',
                'description': '可以流畅阅读英文文档，进行日常交流'
            }
        )
        self.stdout.write(self.style.SUCCESS('创建语言能力成功'))

        # 创建作品集
        portfolio, _ = Portfolio.objects.get_or_create(
            user=user,
            title='个人博客系统',
            defaults={
                'type': 'project',
                'description': '使用Django开发的博客系统',
                'url': 'https://github.com/zhangsan/blog',
                'highlights': '支持Markdown编辑，评论功能，用户管理等'
            }
        )
        self.stdout.write(self.style.SUCCESS('创建作品集成功'))

        # 创建社交链接
        social_link, _ = SocialLink.objects.get_or_create(
            user=user,
            platform='GitHub',
            defaults={
                'url': 'https://github.com/zhangsan',
                'description': '个人GitHub主页'
            }
        )
        self.stdout.write(self.style.SUCCESS('创建社交链接成功'))

        self.stdout.write(self.style.SUCCESS('所有测试数据创建成功')) 