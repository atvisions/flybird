from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from django.db import connection
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from users.profile.models import (
    BasicInfo, JobIntention, WorkExperience, Education,
    Project, Skill, Certificate, Language, Portfolio, SocialLink, ProfileScore
)
from users.signals import (
    create_user_profile, 
    update_basic_dimension_score,
    update_experience_dimension_score,
    update_ability_dimension_score,
    update_achievement_dimension_score
)

User = get_user_model()

class Command(BaseCommand):
    help = '创建一个完整的用户档案'

    def handle(self, *args, **kwargs):
        phone = '13800138000'
        
        # 1. 清理已存在的数据
        with connection.cursor() as cursor:
            # 获取用户ID
            user = User.objects.filter(phone=phone).first()
            if user:
                user_id = user.id
                # 按顺序删除关联数据（注意外键依赖顺序）
                tables = [
                    'users_sociallink',         # 社交链接
                    'users_portfolio',          # 作品集
                    'users_language',           # 语言能力
                    'users_certificate',        # 证书
                    'users_skill',              # 技能
                    'users_project',            # 项目经历
                    'users_education',          # 教育经历
                    'users_workexperience',     # 工作经历
                    'users_jobintention',       # 求职意向
                    'users_profilelayout',      # 档案布局
                ]
                
                # 先删除所有关联数据
                for table in tables:
                    try:
                        cursor.execute(f"DELETE FROM {table} WHERE user_id = %s", [user_id])
                        self.stdout.write(f'从 {table} 删除了数据')
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'删除 {table} 数据时出错: {str(e)}'))
                
                # 删除基本信息
                try:
                    cursor.execute("DELETE FROM user_basic_info WHERE user_id = %s", [user_id])
                    self.stdout.write('基本信息删除成功')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'删除基本信息时出错: {str(e)}'))
                
                # 最后删除用户
                try:
                    cursor.execute("DELETE FROM users_user WHERE id = %s", [user_id])
                    self.stdout.write('用户删除成功')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'删除用户时出错: {str(e)}'))
                    return
    
        # 2. 临时禁用信号
        post_save.disconnect(create_user_profile, sender=User)
        
        try:
            # 3. 创建新用户
            user = User.objects.create_user(
                phone=phone,
                username='complete_profile',
                password='expert123',
                is_staff=True
            )
            
            # 确保 ProfileScore 存在
            score = ProfileScore.objects.create(user=user)
            
            self.stdout.write(self.style.SUCCESS('用户创建成功'))

            # 4. 创建基本信息
            basic_info = BasicInfo.objects.create(
                user=user,
                name='张明',
                gender='male',
                birthday=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
                location='上海',
                email='zhangming@example.com',
                job_title='高级技术专家',
                years_of_experience=10,
                personal_summary='10年互联网研发经验，专注于分布式系统和微服务架构...'
            )
            self.stdout.write(self.style.SUCCESS('基本信息创建成功'))
            
            # 检查评分是否正确更新
            score = user.profile_score
            self.stdout.write(f'基本信息分数: {score.basic_dimension}')
            if score.basic_dimension == 0:
                self.stdout.write(self.style.WARNING('警告：基本信息分数为0'))
                # 手动触发一次评分计算
                update_basic_dimension_score(BasicInfo, basic_info)
                self.stdout.write(f'重新计算后的分数: {score.basic_dimension}')

            # 5. 创建求职意向
            intention = JobIntention.objects.create(
                user=user,
                job_type='full_time',
                expected_salary='50-70k',
                expected_city='上海',
                job_status='open',
                industries='互联网,人工智能'
            )
            self.stdout.write(self.style.SUCCESS('求职意向创建成功'))

            # 6. 创建工作经历
            WorkExperience.objects.create(
                user=user,
                company='阿里巴巴',
                position='技术专家',
                start_date=datetime.strptime('2018-01-01', '%Y-%m-%d').date(),
                end_date=datetime.strptime('2023-12-31', '%Y-%m-%d').date(),
                is_current=True,
                description='负责分布式架构设计和团队管理工作...'
            )
            self.stdout.write(self.style.SUCCESS('工作经历创建成功'))

            # 7. 创建教育经历
            Education.objects.create(
                user=user,
                school='清华大学',
                major='计算机科学与技术',
                degree='master',
                start_date='2008-09-01',
                end_date='2011-07-01',
                description='研究方向：分布式系统...',
            )
            self.stdout.write(self.style.SUCCESS('教育经历创建成功'))

            # 8. 创建项目经历
            Project.objects.create(
                user=user,
                name='分布式事务系统',
                role='技术负责人',
                start_date='2020-01-01',
                end_date='2023-12-31',
                is_current=True,
                description='设计并实现了高可用的分布式事务系统...',
            )
            self.stdout.write(self.style.SUCCESS('项目经历创建成功'))

            # 9. 创建技能特长
            skills = ['Python', 'Java', 'Golang', 'MySQL', 'Redis', 'Kubernetes']
            for skill in skills:
                Skill.objects.create(
                    user=user,
                    name=skill,
                    level='expert'
                )
            self.stdout.write(self.style.SUCCESS('技能特长创建成功'))

            # 10. 创建证书认证
            Certificate.objects.create(
                user=user,
                name='PMP认证',
                type='professional',
                issuing_authority='PMI',
                issue_date='2019-01-01',
                expiry_date='2025-01-01',
            )
            self.stdout.write(self.style.SUCCESS('证书认证创建成功'))

            # 11. 创建语言能力
            Language.objects.create(
                user=user,
                name='英��',
                level='proficient'
            )
            self.stdout.write(self.style.SUCCESS('语言能力创建成功'))

            # 12. 创建作品集
            Portfolio.objects.create(
                user=user,
                title='开源项目',
                description='一个高性能的分布式框架',
                url='https://github.com/zhangming/awesome-project',
            )
            self.stdout.write(self.style.SUCCESS('作品集创建成功'))

            # 13. 创建社交主页
            SocialLink.objects.create(
                user=user,
                platform='GitHub',
                url='https://github.com/zhangming'
            )
            self.stdout.write(self.style.SUCCESS('社交主页创建成功'))

            self.stdout.write(self.style.SUCCESS('完整档案创建成功')) 

            # 显示评分
            score = user.profile_score
            self.stdout.write(f'基础维度分数: {score.basic_dimension}')
            self.stdout.write(f'总分: {score.total_score}')

            # 手动触发评分计算
            self.stdout.write('\n开始计算评分...')
            
            # 计算经验维度分数
            work_exp = WorkExperience.objects.filter(user=user).first()
            if work_exp:
                update_experience_dimension_score(WorkExperience, work_exp)
                # 立即验证分数
                score = ProfileScore.objects.get(user=user)
                self.stdout.write(f'经验维度分数验证: {score.experience_dimension}')
            
            # 计算能力维度分数
            skill = Skill.objects.filter(user=user).first()
            if skill:
                update_ability_dimension_score(Skill, skill)
                # 立即验证分数
                score = ProfileScore.objects.get(user=user)
                self.stdout.write(f'能力维度分数验证: {score.ability_dimension}')
            
            # 计算成就维度分数
            cert = Certificate.objects.filter(user=user).first()
            if cert:
                update_achievement_dimension_score(Certificate, cert)
                # 立即验证分数
                score = ProfileScore.objects.get(user=user)
                self.stdout.write(f'成就维度分数验证: {score.achievement_dimension}')
            
            # 刷新对象并显示最终评分
            score = ProfileScore.objects.get(user=user)
            self.stdout.write('\n最终档案评分结果:')
            self.stdout.write(f'总分: {score.total_score:.1f}\n')
            self.stdout.write('维度得分:')
            self.stdout.write(f'- 基础维度: {score.basic_dimension} (权重: 0.4)')
            self.stdout.write(f'- 经验维度: {score.experience_dimension} (权重: 0.3)')
            self.stdout.write(f'- 能力维度: {score.ability_dimension} (权重: 0.2)')
            self.stdout.write(f'- 成就维度: {score.achievement_dimension} (权重: 0.1)')
            
            # 计算加权总分
            weighted_score = (
                score.basic_dimension * 0.4 +
                score.experience_dimension * 0.3 +
                score.ability_dimension * 0.2 +
                score.achievement_dimension * 0.1
            )
            self.stdout.write(f'\n加权总分: {weighted_score:.1f}')

        finally:
            # 重新连接信号
            post_save.connect(create_user_profile, sender=User) 