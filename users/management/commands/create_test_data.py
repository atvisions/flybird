from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.profile.models import (
    BasicInfo, JobIntention, WorkExperience, Education,
    Project, Skill, Certificate, Language, Portfolio, SocialLink
)

User = get_user_model()

class Command(BaseCommand):
    help = '创建测试用户和档案数据'

    def handle(self, *args, **kwargs):
        # 1. 创建用户
        user, created = User.objects.get_or_create(
            phone='13800138000',
            defaults={
                'username': 'liuqiang',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('用户创建成功'))
        
        # 2. 基本信息
        basic_info, created = BasicInfo.objects.get_or_create(
            user=user,
            defaults={
                'name': '刘强',
                'gender': 'male',
                'birthday': '1992-03-15',
                'location': '上海市浦东新区',
                'job_title': '高级全栈工程师',
                'bio': '8年全栈开发经验，专注于大规模分布式系统架构设计和前端工程化实践。\n'
                      '擅长 Python/Java 后端开发和 React 前端开发，对微服务架构、云原生技术有深入研究。\n'
                      '热衷技术分享，在掘金、知乎等平台发表过多篇技术文章，GitHub 个人项目 1k+ star。',
                'email': 'liuqiang@example.com'
            }
        )
        
        # 3. 求职意向
        job_intention, created = JobIntention.objects.get_or_create(
            user=user,
            defaults={
                'job_type': '全职',
                'expected_salary': '40-60K',
                'expected_city': '上海',
                'job_status': '在职看机会',
                'description': '期望加入技术驱动型公司，担任技术专家或架构师职位。\n'
                             '擅长系统架构设计、性能优化、团队管理，能带领团队完成高质量交付。\n'
                             '希望在云原生、微服务架构等领域有更深的实践。'
            }
        )
        
        # 4. 工作经历
        work1, created = WorkExperience.objects.get_or_create(
            user=user,
            company='字节跳动',
            defaults={
                'position': '技术专家',
                'start_date': '2020-06-01',
                'is_current': True,
                'description': '负责抖音电商核心系统的架构设计和团队管理工作：\n'
                             '1. 主导完成订单系统微服务改造��将系统性能提升3倍，支持日订单量过亿\n'
                             '2. 设计实现分布式事务解决方案，确保交易系统数据一致性\n'
                             '3. 优化系统监控和告警体系，将故障发现时间从分钟级降至秒级\n'
                             '4. 带领20人团队，建立完整的开发规范和质量保证体系\n'
                             '5. 主导技术选型和架构评审，指导团队进行技术攻关'
            }
        )
        
        work2, created = WorkExperience.objects.get_or_create(
            user=user,
            company='阿里巴巴',
            defaults={
                'position': '高级开发工程师',
                'start_date': '2017-07-01',
                'end_date': '2020-05-31',
                'is_current': False,
                'description': '参与淘宝交易平台核心系统开发：\n'
                             '1. 负责交易系统性能优化，将下单耗时降低40%，支持双11千万级并发\n'
                             '2. 设计实现分布式限流框架，有效保护系统稳定性\n'
                             '3. 主导服务治理平台开发，提升微服务运维效率\n'
                             '4. 参与中间件技术攻关，解决跨数据中心数据同步等难题\n'
                             '5. 获得年度最佳工程师称号'
            }
        )
        
        # 5. 教育经历
        education, created = Education.objects.get_or_create(
            user=user,
            school='浙江大学',
            defaults={
                'major': '软件工程',
                'degree': '硕士',
                'start_date': '2014-09-01',
                'end_date': '2017-07-01',
                'is_current': False,
                'description': '研究方向：分布式系统\n'
                             '主修课程：高级软件工程、分布式计算、云计算、数据挖掘\n'
                             '成果：\n'
                             '- 发表SCI论文2篇，申请发明专利1项\n'
                             '- 获得国家奖学金、优秀毕业生等荣誉\n'
                             '- 参与国家自然科学基金项目研究'
            }
        )
        
        # 6. 项目经历
        project1, created = Project.objects.get_or_create(
            user=user,
            name='抖音电商订单系统重构',
            defaults={
                'role': '技术负责人',
                'start_date': '2021-03-01',
                'end_date': '2022-06-30',
                'is_current': False,
                'description': '带领团队完成订单系统从单体应用到微服务架构的转型\n'
                             '1. 设计微服务拆分方案，实现业务解耦\n'
                             '2. 使用DDD领域驱动设计指导系统设计\n'
                             '3. 基于K8s构建容器化部署平台\n'
                             '4. 实现灰度发布和自动化运维体系',
                'achievement': '1. 系统吞吐量提升300%，支持日订单量1亿+\n'
                             '2. 服务可用性达到99.99%\n'
                             '3. 开发效率提升50%，测试覆盖率达到85%\n'
                             '4. 获得公司年度最佳项目奖'
            }
        )
        
        project2, created = Project.objects.get_or_create(
            user=user,
            name='分布式限流框架',
            defaults={
                'role': '核心开发者',
                'start_date': '2019-06-01',
                'end_date': '2019-12-31',
                'is_current': False,
                'description': '设计实现一个高性能分布式限流框架：\n'
                             '1. 基于Redis实现分布式令牌桶算法\n'
                             '2. 支持多维度限流策略和动态配置\n'
                             '3. 提供实时监控和告警功能\n'
                             '4. 封装SDK便于业务入',
                'achievement': '1. 已在公司内部广泛使用，接入服务数100+\n'
                             '2. 支持百万级QPS限流场景\n'
                             '3. 获得内部开源项目推荐\n'
                             '4. 相关技术方案发表在公司技术博客'
            }
        )
        
        # 7. 技能特长
        skills = [
            ('后端开发', '精通', 'Java/Python/Go等语言开发，熟悉Spring Cloud、Django等框架'),
            ('前端开发', '熟练', 'React/Vue技术栈，了解前端工程化和性能优化'),
            ('系统架构', '精通', '微服务架构设计、DDD实践、性能优化、高可用设计'),
            ('中间件', '精通', '深入了解Redis、MySQL、Kafka、Elasticsearch等'),
            ('云原生', '熟练', '熟悉Docker、K8s、服务网格、云原生架构设计'),
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
            ('AWS解决方案架构师专家级认证', 'professional', 'Amazon', '2022-06-15'),
            ('PMP项目管理专业人士认证', 'professional', 'PMI', '2021-08-20'),
            ('阿里云高级技术专家认证', 'professional', '阿里云', '2020-11-30'),
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
            ('英语', '精通', 'TOEFL 105分，可流畅进行英文技术交流和文档写作'),
            ('日语', '良好', 'N2水平，可进行日常交流和简单技术沟通'),
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
            ('分布式任务调度平台', '基于Go开发的分布式任务调度系统，支持cron和实时任务，GitHub 1.2k star', 'https://github.com/liuqiang/task-scheduler'),
            ('React组件库', '企业级React组件库，包含50+组件，完善的文档和测试', 'https://github.com/liuqiang/react-components'),
            ('技术博客', '个人技术博客，主要分享架构设计和技术实践经验', 'https://blog.liuqiang.com'),
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
            ('GitHub', 'https://github.com/liuqiang', '开源项目展示'),
            ('掘金', 'https://juejin.cn/user/liuqiang', '技术博客'),
            ('知乎', 'https://www.zhihu.com/people/liuqiang', '技术问答'),
            ('LinkedIn', 'https://www.linkedin.com/in/liuqiang', '职业经历'),
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
        
        self.stdout.write(self.style.SUCCESS('所有测试数据创建成功')) 