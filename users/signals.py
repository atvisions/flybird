from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from users.profile.models import BasicInfo, WorkExperience, Education, Project, Skill, Certificate, Language, Portfolio
from users.profile.models.layout import ProfileLayout
from users.models import ProfileScore

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
    """更新基础维度分数"""
    print("\n开始计算基础维度分数...")
    print(f"用户: {instance.user.phone}")
    print(f"姓名: {instance.name}")
    print(f"性别: {instance.gender}")
    print(f"生日: {instance.birth_date}")
    print(f"头像: {instance.avatar}")
    print(f"个人简介: {instance.personal_summary}")
    
    # 计算基础维度分数
    score = 0
    
    # 头像 20分
    if instance.avatar:
        score += 20
        
    # 个人简介 20分
    if instance.personal_summary:
        if len(instance.personal_summary) >= 100:
            score += 20
        else:
            score += 10
            
    # 其他基本信息 30分
    if instance.name:
        score += 10
    if instance.gender:
        score += 5
    if instance.birth_date:
        score += 5
    if instance.phone:
        score += 5
    if instance.email:
        score += 5
        
    # 更新分数
    profile_score, _ = ProfileScore.objects.get_or_create(user=instance.user)
    profile_score.basic_dimension = score
    profile_score.save()
    
    print(f"基础维度分数: {score}")

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