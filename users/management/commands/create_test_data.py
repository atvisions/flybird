from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.profile.models import (
    BasicInfo, JobIntention, WorkExperience, Education,
    Project, Skill, Certificate, Language, Portfolio, SocialLink
)
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = '创建测试用户和档案数据'

    def handle(self, *args, **kwargs):
        # 1. 创建用户
        try:
            User.objects.get(phone='13800138000').delete()
        except User.DoesNotExist:
            pass
        
        user = User.objects.create_user(
            phone='13800138000',
            username='test_user',
            password='password123'
        )
        self.stdout.write(self.style.SUCCESS('用户创建成功'))
        
        # 2. 基本信息
        basic_info, created = BasicInfo.objects.get_or_create(
            user=user,
            defaults={
                'name': '张三',
                'gender': 'male',
                'birthday': '1995-01-01',
                'location': '北京市朝阳区',
                'job_title': 'Python开发工程师',
                'bio': '5年Python开发经验，专注于后端开发和系统架构设计',
                'email': 'zhangsan@example.com'
            }
        )
        
        # 3. 求职意向
        job_intention, created = JobIntention.objects.get_or_create(
            user=user,
            defaults={
                'job_type': '全职',
                'expected_salary': '25-35K',
                'expected_city': '北京',
                'job_status': '在职找工作',
                'description': '期望从事Python后端开发工作，擅长Django开发'
            }
        )
        
        # 4. 工作经历
        work1, created = WorkExperience.objects.get_or_create(
            user=user,
            company='ABC科技有限公司',
            defaults={
                'position': '高级后端工程师',
                'start_date': '2020-06-01',
                'end_date': '2023-05-31',
                'is_current': False,
                'is_internship': False,
                'description': '1. 负责公司核心业务系统的后端开发和维护\n2. 优化系统性能，将接口响应时间降低50%\n3. 带领5人团队完成新功能开发'
            }
        )
        
        work2, created = WorkExperience.objects.get_or_create(
            user=user,
            company='XYZ互联网公司',
            defaults={
                'position': 'Python开发工程师',
                'start_date': '2018-07-01',
                'end_date': '2020-05-31',
                'is_current': False,
                'description': '1. 参与电商系统的开发和维护\n2. 实现订单系统重构，提升系统稳定性\n3. 开发自动化测试框架，提高测试效率'
            }
        )
        
        work3, created = WorkExperience.objects.get_or_create(
            user=user,
            company='实习公司',
            defaults={
                'position': '后端开发实习生',
                'start_date': '2018-01-01',
                'end_date': '2018-06-30',
                'is_current': False,
                'is_internship': True,
                'description': '1. 参与后端API开发\n2. 编写单元测试\n3. 参与code review'
            }
        )
        
        # 5. 教育经历
        education, created = Education.objects.get_or_create(
            user=user,
            school='北京大学',
            defaults={
                'major': '计算机科学与技术',
                'degree': '本科',
                'start_date': '2014-09-01',
                'end_date': '2018-07-01',
                'is_current': False,
                'description': '主修课程：数据结构、算法设计、计算机网络、数据库系统'
            }
        )
        
        # 6. 项目经历
        project, created = Project.objects.get_or_create(
            user=user,
            name='电商平台重构项目',
            defaults={
                'role': '技术负责人',
                'start_date': '2021-03-01',
                'end_date': '2021-12-31',
                'is_current': False,
                'description': '带领团队完成电商平台的整体重构，采用微服务架构，提升系统性能和可扩展性',
                'achievement': '1. 系统响应时间降低70%\n2. 支持千万级用户同时在线\n3. 系统可用性达到99.99%'
            }
        )
        
        # 7. 技能特长
        skill1, created = Skill.objects.get_or_create(
            user=user,
            name='Python',
            defaults={
                'level': '精通',
                'description': '熟练使用Python进行后端开发，熟悉Django、Flask等框架'
            }
        )
        
        skill2, created = Skill.objects.get_or_create(
            user=user,
            name='MySQL',
            defaults={
                'level': '熟练',
                'description': '熟悉MySQL数据库设计和优化'
            }
        )
        
        # 8. 语言能力
        language, created = Language.objects.get_or_create(
            user=user,
            name='英语',
            defaults={
                'level': '专业四级',
                'description': '可以流畅阅读英文技术文档，进行日常交流'
            }
        )
        
        # 9. 作品集
        portfolio, created = Portfolio.objects.get_or_create(
            user=user,
            title='开源项目：Python Web框架',
            defaults={
                'description': '一个轻量级的Python Web框架，支持异步请求处理',
                'url': 'https://github.com/zhangsan/web-framework'
            }
        )
        
        # 10. 社交主页
        social_link, created = SocialLink.objects.get_or_create(
            user=user,
            platform='GitHub',
            defaults={
                'url': 'https://github.com/zhangsan'
            }
        )
        
        # 8. 证书
        certificate1, created = Certificate.objects.get_or_create(
            user=user,
            name='PMP项目管理认证',
            defaults={
                'type': 'professional',  # 专业证书
                'issuing_authority': 'PMI',
                'issue_date': '2022-06-15',
                'credential_id': 'PMP123456',
                'description': '项目管理专业人士认证'
            }
        )
        
        certificate2, created = Certificate.objects.get_or_create(
            user=user,
            name='优秀员工奖',
            defaults={
                'type': 'award',  # 获奖证书
                'issuing_authority': 'ABC科技有限公司',
                'issue_date': '2022-12-30',
                'description': '2022年度优秀员工'
            }
        )
        
        certificate3, created = Certificate.objects.get_or_create(
            user=user,
            name='托福考试',
            defaults={
                'type': 'language',  # 语言证书
                'issuing_authority': 'ETS',
                'issue_date': '2021-08-15',
                'credential_id': 'TOEFL123456',
                'description': '总分105分'
            }
        )
        
        self.stdout.write(self.style.SUCCESS('所有测试数据创建成功')) 