from users.profile.models import (
    BasicInfo, WorkExperience, Education, Project,
    Skill, Certificate, Language, Portfolio, SocialLink
)

def calculate_profile_score(user):
    """计算用户档案评分"""
    # 初始化各维度得分
    basic_score = calculate_basic_score(user)
    experience_score = calculate_experience_score(user)
    capability_score = calculate_capability_score(user)
    achievement_score = calculate_achievement_score(user)
    
    # 权重配置
    weights = {
        'basic_dimension': 0.4,      # 基础维度权重
        'experience_dimension': 0.3,  # 经验维度权重
        'capability_dimension': 0.2,  # 能力维度权重
        'achievement_dimension': 0.1  # 成就维度权重
    }
    
    # 计算总分
    total_score = (
        basic_score * weights['basic_dimension'] +
        experience_score * weights['experience_dimension'] +
        capability_score * weights['capability_dimension'] +
        achievement_score * weights['achievement_dimension']
    )
    
    # 生成改进建议
    suggestions = generate_improvement_suggestions(user)
    
    return {
        'total_score': round(total_score, 1),
        'basic_dimension': {
            'score': basic_score,
            'weight': weights['basic_dimension'],
            'weighted_score': round(basic_score * weights['basic_dimension'], 1)
        },
        'experience_dimension': {
            'score': experience_score,
            'weight': weights['experience_dimension'],
            'weighted_score': round(experience_score * weights['experience_dimension'], 1)
        },
        'capability_dimension': {
            'score': capability_score,
            'weight': weights['capability_dimension'],
            'weighted_score': round(capability_score * weights['capability_dimension'], 1)
        },
        'achievement_dimension': {
            'score': achievement_score,
            'weight': weights['achievement_dimension'],
            'weighted_score': round(achievement_score * weights['achievement_dimension'], 1)
        },
        'improvement_suggestions': suggestions
    }

def calculate_basic_score(user):
    """计算基础维度得分"""
    score = 0
    try:
        basic_info = user.basicinfo
        
        # 1. 基本信息完整性评分 (总分40分)
        if basic_info.name: score += 10        # 姓名
        if basic_info.avatar: score += 5       # 头像
        if basic_info.gender: score += 5       # 性别
        if basic_info.birthday: score += 5     # 生日
        if basic_info.location: score += 5     # 所在地
        if basic_info.email: score += 5        # 邮箱
        if basic_info.job_title: score += 5    # 职位
        
        # 2. 工作年限评分 (总分20分)
        if basic_info.years_of_experience:
            score += min(basic_info.years_of_experience * 2, 20)
            
        # 3. 个人简介评分 (总分20分)
        if basic_info.personal_summary:
            # 根据字数评分
            length = len(basic_info.personal_summary)
            if length >= 200: score += 20
            elif length >= 100: score += 15
            elif length >= 50: score += 10
            else: score += 5
        
        # 4. 求职意向完整性评分 (总分20分)
        try:
            intention = user.jobintention
            if intention.job_type: score += 5
            if intention.expected_salary: score += 5
            if intention.expected_city: score += 5
            if intention.industry_preference: score += 5
        except:
            pass
            
    except:
        pass
    
    return min(score, 100)  # 确保不超过100分

def calculate_experience_score(user):
    """计算经验维度得分"""
    score = 0
    try:
        # 工作经历评分
        work_exp_count = WorkExperience.objects.filter(user=user).count()
        score += min(work_exp_count * 10, 30)  # 最高30分
        
        # 教育经历评分
        edu_count = Education.objects.filter(user=user).count()
        score += min(edu_count * 10, 20)  # 最高20分
        
        # 项目经历评分
        project_count = Project.objects.filter(user=user).count()
        score += min(project_count * 10, 20)  # 最高20分
    except:
        pass
    return min(score, 100)

def calculate_capability_score(user):
    """计算能力维度得分"""
    score = 0
    try:
        # 技能评分
        skill_count = Skill.objects.filter(user=user).count()
        score += min(skill_count * 5, 20)  # 最高20分
        
        # 语言能力评分
        language_count = Language.objects.filter(user=user).count()
        score += min(language_count * 10, 20)  # 最高20分
    except:
        pass
    return min(score, 100)

def calculate_achievement_score(user):
    """计算成就维度得分"""
    score = 0
    try:
        # 证书评分
        cert_count = Certificate.objects.filter(user=user).count()
        score += min(cert_count * 5, 20)  # 最高20分
        
        # 作品集评分
        portfolio_count = Portfolio.objects.filter(user=user).count()
        score += min(portfolio_count * 10, 20)  # 最高20分
        
        # 社交主页评分
        social_count = SocialLink.objects.filter(user=user).count()
        score += min(social_count * 5, 10)  # 最高10分
    except:
        pass
    return min(score, 100)

def generate_improvement_suggestions(user):
    """生成改进建议"""
    suggestions = []
    try:
        basic_info = user.basicinfo
        if not basic_info.avatar:
            suggestions.append({
                'field': 'avatar',
                'message': '添加头像可以让你的档案更加专业',
                'score_impact': 5
            })
    except:
        pass
    return suggestions 