from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from users.profile.models import BasicInfo, WorkExperience, Education, Project, Skill, Certificate, Language, Portfolio
from users.profile.models.layout import ProfileLayout
from users.profile.models.score import ProfileScore

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """创建用户时自动创建基本信息和档案布局"""
    if created:
        # 创建档案评分（放在最前面）
        ProfileScore.objects.create(user=instance)
        
        # 只在不存在时创建基本信息
        BasicInfo.objects.get_or_create(user=instance)
        
        # 只在不存在时创建档案布局
        ProfileLayout.objects.get_or_create(
            user=instance,
            defaults={
                'layout': {
                    'basic_info': {'order': 1, 'visible': True},
                    'job_intention': {'order': 2, 'visible': True},
                    'work_experience': {'order': 3, 'visible': True},
                    'education': {'order': 4, 'visible': True},
                    'project': {'order': 5, 'visible': True},
                    'skill': {'order': 6, 'visible': True},
                    'certificate': {'order': 7, 'visible': True},
                    'language': {'order': 8, 'visible': True},
                    'portfolio': {'order': 9, 'visible': True},
                    'social_link': {'order': 10, 'visible': True}
                }
            }
        )

@receiver(post_save, sender=BasicInfo)
def update_basic_dimension_score(sender, instance, **kwargs):
    """当基本信息更新时，重新计算基础维度分数"""
    print("\n开始计算基础维度分数...")
    print(f"用户: {instance.user.phone}")
    print(f"姓名: {instance.name}")
    print(f"性别: {instance.gender}")
    print(f"生日: {instance.birthday}")
    print(f"地点: {instance.location}")
    print(f"邮箱: {instance.email}")
    print(f"职位: {instance.job_title}")
    print(f"工作年限: {instance.years_of_experience}")
    print(f"个人简介长度: {len(instance.personal_summary) if instance.personal_summary else 0}")
    
    # 确保 profile_score 存在
    score, created = ProfileScore.objects.get_or_create(user=instance.user)
    
    points = 0
    
    # 基础信息 (总分70分)
    if instance.avatar:
        points += 20  # 头像很重要，保持20分
        print(f"头像: +20分")
    if instance.name:
        points += 10  # 姓名也很重要
        print(f"姓名: +10分")
    if instance.gender:
        points += 5
        print(f"性别: +5分")
    if instance.birthday:
        points += 5
        print(f"生日: +5分")
    if instance.location:
        points += 5
        print(f"所在地: +5分")
    if instance.email:
        points += 5
        print(f"邮箱: +5分")
    if instance.job_title:
        points += 10  # 职位信息提高到10分
        print(f"职位: +10分")
    if instance.years_of_experience is not None:
        points += 5
        print(f"工作年限: +5分")
    if instance.personal_summary:
        points += 15  # 个人简介提高到15分
        print(f"个人简介: +15分")
    
    # 质量加分 (最高30分)
    if instance.personal_summary and len(instance.personal_summary) >= 100:
        points += 10  # 详细的个人简介
        print(f"详细简介: +10分")
    if instance.avatar and hasattr(instance.avatar, 'size') and instance.avatar.size >= 100 * 1024:  # 高清头像
        points += 10
        print(f"高清头像: +10分")
    if instance.years_of_experience and instance.years_of_experience >= 5:
        points += 10  # 资深工作经验
        print(f"资深经验: +10分")
    
    print(f"基础维度总得分: {points}")
    
    score.basic_dimension = points
    score.save()
    print(f"基础维度分数已保存: {score.basic_dimension}")

@receiver(post_save, sender=WorkExperience)
@receiver(post_save, sender=Education)
def update_experience_dimension_score(sender, instance, **kwargs):
    """当工作经历或教育经历更新时，重新计算经验维度分数"""
    print(f"更新经验维度分数 - 用户: {instance.user.phone}")
    
    # 确保 profile_score 存在
    score, created = ProfileScore.objects.get_or_create(user=instance.user)
    print(f"当前经验维度分数: {score.experience_dimension}")
    
    # 工作经历得分
    work_count = WorkExperience.objects.filter(user=instance.user).count()
    work_score = min(work_count * 20, 60)  # 每段20分，最高60分
    print(f"工作经历数量: {work_count}, 得分: {work_score}")
    
    # 教育经历得分
    edu_count = Education.objects.filter(user=instance.user).count()
    edu_score = min(edu_count * 30, 40)  # 每段30分，最高40分
    print(f"教育经历数量: {edu_count}, 得分: {edu_score}")
    
    total_score = work_score + edu_score
    print(f"经验维度总分: {total_score}")
    
    score.experience_dimension = total_score
    score.save()
    print(f"保存后的经验维度分数: {score.experience_dimension}")
    
    # 重新获取对象验证分数
    score_check = ProfileScore.objects.get(user=instance.user)
    print(f"验证经验维度分数: {score_check.experience_dimension}")

@receiver(post_save, sender=Skill)
@receiver(post_save, sender=Language)
def update_ability_dimension_score(sender, instance, **kwargs):
    """当技能或语言能力更新时，重新计算能力维度分数"""
    print(f"更新能力维度分数 - 用户: {instance.user.phone}")  # 添加日志
    
    # 确保 profile_score 存在
    score, created = ProfileScore.objects.get_or_create(user=instance.user)
    
    # 技能得分
    skill_count = Skill.objects.filter(user=instance.user).count()
    skill_score = min(skill_count * 12, 60)  # 每个技能12分，5个技能即可满分
    print(f"技能数量: {skill_count}, 得分: {skill_score}")
    
    # 语言得分
    lang_count = Language.objects.filter(user=instance.user).count()
    lang_score = min(lang_count * 20, 40)  # 每门语言20分，2门语言满分
    print(f"语言数量: {lang_count}, 得分: {lang_score}")
    
    total_score = skill_score + lang_score
    print(f"能力维度总分: {total_score}")
    
    score.ability_dimension = total_score
    score.save()

@receiver(post_save, sender=Certificate)
@receiver(post_save, sender=Portfolio)
def update_achievement_dimension_score(sender, instance, **kwargs):
    """当证书或作品集更新时，重新计算成就维度分数"""
    print(f"更新成就维度分数 - 用户: {instance.user.phone}")  # 添加日志
    
    # 确保 profile_score 存在
    score, created = ProfileScore.objects.get_or_create(user=instance.user)
    
    # 证书得分
    cert_count = Certificate.objects.filter(user=instance.user).count()
    cert_score = min(cert_count * 25, 60)  # 每个证书25分，满分需要3个证书
    print(f"证书数量: {cert_count}, 得分: {cert_score}")
    
    # 作品集得分
    port_count = Portfolio.objects.filter(user=instance.user).count()
    port_score = min(port_count * 20, 40)  # 每个作品20分，2个作品满分
    print(f"作品数量: {port_count}, 得分: {port_score}")
    
    total_score = cert_score + port_score
    print(f"成就维度总分: {total_score}")
    
    score.achievement_dimension = total_score
    score.save() 