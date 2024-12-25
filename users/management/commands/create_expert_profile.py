from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
import requests
from users.profile.models import (
    BasicInfo, JobIntention, WorkExperience, Education,
    Project, Skill, Certificate, Language, Portfolio, SocialLink, ProfileScore
)

User = get_user_model()

class Command(BaseCommand):
    help = '创建高级技术专家档案数据'

    def handle(self, *args, **kwargs):
        # 1. 创建用户
        user, created = User.objects.get_or_create(
            phone='13900139000',
            defaults={
                'username': 'techexpert',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        # 确保用户和 ProfileScore 都存在
        if created:
            user.set_password('expert123')
            user.save()
        
        # 无论是否是新用户，都确保 ProfileScore 存在
        score, score_created = ProfileScore.objects.get_or_create(user=user)
        
        self.stdout.write(f'用户数据验证: {User.objects.filter(phone="13900139000").exists()}')
        
        # 2. 基本信息
        basic_info = BasicInfo.objects.filter(user=user).first()
        if basic_info:
            # 如果存在就更新
            for key, value in {
                'name': '张明',
                'gender': 'male',
                'birthday': '1988-06-15',
                'location': '北京市朝阳区',
                'job_title': '技术总监/架构师',
                'personal_summary': '15年互联网研发和架构经验，专注于分布式系统、微服务架构和中台建设。\n'
                      '曾主导多个大型技术中台和核心系统的架构设计与建设，\n'
                      '在高并发、分布式架构、微服务治理等方面有丰富经验。\n'
                      '负责过百人级研发团队管理，推动技术创新和架构升级。',
                'email': 'zhangming@example.com',
                'years_of_experience': 15
            }.items():
                setattr(basic_info, key, value)
            basic_info.save()  # 这会触发 post_save 信号
        else:
            # 如果不存在就创建
            basic_info = BasicInfo.objects.create(
                user=user,
                name='张明',
                gender='male',
                birthday='1988-06-15',
                location='北京��朝阳区',
                job_title='技术总监/架构师',
                personal_summary='15年互联网研发和架构经验，专注于分布式系统、微服务架构和中台建设。\n'
                      '曾主导多个大型技术中台和核心系统的架构设计与建设，\n'
                      '在高并发、分布式架构、微服务治理等方面有丰富经验。\n'
                      '负责过百人级研发团队管理，推动技术创新和架构升级。',
                email='zhangming@example.com',
                years_of_experience=15
            )
        
        self.stdout.write(f'基本信息验证: {BasicInfo.objects.filter(user=user).exists()}')
        
        # 3. 求职意向
        job_intention, created = JobIntention.objects.get_or_create(
            user=user,
            defaults={
                'job_type': 'full_time',
                'expected_salary': '80-120K',
                'expected_city': '北京',
                'job_status': 'open',
                'industries': '互联网,人工智能'
            }
        )
        
        # 4. 工作经历
        works = [
            {
                'company': '腾讯',
                'position': '技术总监',
                'start_date': '2020-01-01',
                'is_current': True,
                'description': '负责腾讯云原生中台建设和架构升级：\n'
                             '1. 主导完成全公司级中台战略规划和架构设计\n'
                             '2. 带领200人团队完成多个核心系统重构和升级\n'
                             '3. 建立完整的微服务治理体系和技术标准\n'
                             '4. 推动DevOps落地，研发效率提升200%\n'
                             '5. 多次获得年度最佳技术团队奖'
            },
            {
                'company': '阿里巴巴',
                'position': '高级技术专家',
                'start_date': '2016-03-01',
                'end_date': '2019-12-31',
                'description': '负责淘宝交易核心系统架构设计：\n'
                             '1. 设计实现全链路压测平台，支持百万级并发测试\n'
                             '2. 主导交易系统微服务改造，拆分200+服务\n'
                             '3. 设计分布式事务框架，成为集团统一标准\n'
                             '4. 负责双11核心系统架构设计和保障\n'
                             '5. 获得年度最佳架构师称号'
            },
            {
                'company': '百度',
                'position': '资深研发工程师',
                'start_date': '2012-07-01',
                'end_date': '2016-02-29',
                'description': '负责百度搜索引擎核心组件开发：\n'
                             '1. 设计实现分布式爬虫系统，日处理PB级数据\n'
                             '2. 优化搜索引擎性能，响应时间降低40%\n'
                             '3. 开发实时索引系统，时效性提升10倍\n'
                             '4. 获得多项技术专利'
            }
        ]
        
        for work in works:
            work_exp, created = WorkExperience.objects.get_or_create(
                user=user,
                company=work['company'],
                position=work['position'],
                defaults={
                    'start_date': work['start_date'],
                    'end_date': work.get('end_date'),
                    'is_current': work.get('is_current', False),
                    'description': work['description']
                }
            )
        
        self.stdout.write(f'工作经历数量: {WorkExperience.objects.filter(user=user).count()}')
        
        # 5. 教育经历
        Education.objects.get_or_create(
            user=user,
            school='清华大学',
            defaults={
                'major': '计算机科学与技术',
                'degree': '硕士',
                'start_date': '2009-09-01',
                'end_date': '2012-07-01',
                'description': '研究方向：分布式系统与并行计算\n'
                             '要成果：\n'
                             '- 发表顶级会议论文3篇\n'
                             '- 获得国家奖学金\n'
                             '- 参与国家863项目研究'
            }
        )
        
        # 6. 项目经历
        projects = [
            {
                'name': '腾讯云原生中台建设',
                'role': '总架构师',
                'start_date': '2020-03-01',
                'is_current': True,
                'description': '全面负责腾讯云原生中台的架构设计和建设：\n'
                             '1. 设计云原生技术架构，包括服务网格、容器编排、微服务治理等\n'
                             '2. 建立DevOps平台，支持千级集群管理\n'
                             '3. 实现多云统一管理平台\n'
                             '4. 建设统一监控和运维平台',
                'achievement': '1. 支持集团所有业务线云原生化改造\n'
                             '2. 研发效率提升200%，运维成本降低60%\n'
                             '3. 获得CNCF最���实践奖\n'
                             '4. 相关实践发表于QCon、ArchSummit等顶级会议'
            },
            {
                'name': '淘宝交易系统改造',
                'role': '架构负责人',
                'start_date': '2017-06-01',
                'end_date': '2019-12-31',
                'description': '负责淘宝交易核心系统的微服务改造：\n'
                             '1. 设计DDD领域模型，指导服务拆分\n'
                             '2. 实现分布式事务框架\n'
                             '3. 设计限流、熔断、降级等容错机制\n'
                             '4. 建立性能监控和预警体系',
                'achievement': '1. 系统可用性达到99.999%\n'
                             '2. 支持双11万TPS\n'
                             '3. 服务响应时间降低50%\n'
                             '4. 获得年度最佳架构奖'
            }
        ]
        
        for project in projects:
            Project.objects.get_or_create(
                user=user,
                name=project['name'],
                defaults={
                    'role': project['role'],
                    'start_date': project['start_date'],
                    'end_date': project.get('end_date'),
                    'is_current': project.get('is_current', False),
                    'description': project['description'],
                    'achievement': project['achievement']
                }
            )
        
        # 7. 技能特长
        skills = [
            ('架构设计', '精通', '微服务架构、DDD实践、分布式系统设计、高可用架构'),
            ('云原生技术', '精通', 'Kubernetes、Service Mesh、Docker、云原生架构设计'),
            ('编程语言', '精通', 'Java、Go、Python、JavaScript等全栈术'),
            ('中间件', '精通', 'MySQL、Redis、Kafka、ElasticSearch等分布式中间件'),
            ('团队管理', '精通', '技术团队管理、技术战略规划、研发流程优化'),
        ]
        
        for name, level, desc in skills:
            Skill.objects.get_or_create(
                user=user,
                name=name,
                defaults={
                    'level': level,
                    'description': desc
                }
            )
        
        # 8. 证书
        certificates = [
            ('CNCF CKA认证', 'professional', 'CNCF', '2023-01-15'),
            ('AWS解决方案架构师专家认证', 'professional', 'Amazon', '2022-06-20'),
            ('PMP认证', 'professional', 'PMI', '2021-08-10'),
            ('阿里云技术专家认证', 'professional', '阿里云', '2019-11-30'),
        ]
        
        for name, type, authority, date in certificates:
            Certificate.objects.get_or_create(
                user=user,
                name=name,
                defaults={
                    'type': type,
                    'issuing_authority': authority,
                    'issue_date': date,
                }
            )
        
        # 9. 语言能力
        languages = [
            ('英语', '精通', 'TOEFL 110分，可流畅进行英文技术交流和演讲'),
            ('日语', '良好', 'N1级，可进行技术交流和文档阅读'),
        ]
        
        for name, level, desc in languages:
            Language.objects.get_or_create(
                user=user,
                name=name,
                defaults={
                    'level': level,
                    'description': desc
                }
            )
        
        # 10. 作品集
        portfolios = [
            ('分布式事务框架', '基于TCC模式的分布式事务框架，已开源并广泛使用，GitHub 3k+ stars', 'https://github.com/zhangming/dtx'),
            ('云原生监控平台', '统一的云原生监控解决方案，支持多云管理，2k+ stars', 'https://github.com/zhangming/cloudmonitor'),
            ('技术博客', '分享架构设计和技术管理经验，月访问量10w+', 'https://blog.zhangming.dev'),
            ('技术专栏', '《深入理解分布式架构》专栏作者，订阅量5w+', 'https://column.zhangming.dev'),
        ]
        
        for title, desc, url in portfolios:
            Portfolio.objects.get_or_create(
                user=user,
                title=title,
                defaults={
                    'description': desc,
                    'url': url
                }
            )
        
        # 11. 社交主页
        social_links = [
            ('GitHub', 'https://github.com/zhangming', '开源项目展示'),
            ('知乎', 'https://www.zhihu.com/people/zhangming', '技术专栏作者'),
            ('InfoQ', 'https://www.infoq.cn/profile/zhangming', '技术社区专家'),
            ('LinkedIn', 'https://www.linkedin.com/in/zhangming', '职业经历'),
        ]
        
        for platform, url, desc in social_links:
            SocialLink.objects.get_or_create(
                user=user,
                platform=platform,
                defaults={
                    'url': url,
                    'description': desc
                }
            )
        
        self.stdout.write(self.style.SUCCESS('高级技术专家档案创建成功')) 
        
        # 在创建完所有数据后，验证评分
        score = ProfileScore.objects.get(user=user)
        self.stdout.write('\n档案评分结果:')
        self.stdout.write(f'基础维度: {score.basic_dimension}')
        self.stdout.write(f'经验维度: {score.experience_dimension}')
        self.stdout.write(f'能力维度: {score.ability_dimension}')
        self.stdout.write(f'成就维度: {score.achievement_dimension}')
        self.stdout.write(f'总分: {score.total_score}')

    def get_token(self, user):
        """获取用户的认证令牌"""
        try:
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/auth/login/',
                json={
                    'phone': user.phone,
                    'password': 'expert123'
                }
            )
            if response.status_code == 200:
                return response.json()['access']
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'获取令牌失败：{str(e)}'))
        return None 