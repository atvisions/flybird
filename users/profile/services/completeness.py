from django.db.models import Count, Q
from django.utils import timezone
from ..models import (
    BasicInfo, JobIntention, WorkExperience, Education,
    Skill, Project, Certificate, Language, Portfolio, SocialLink
)

class CompletenessCalculator:
    def calculate_completeness(self, user):
        """计算用户档案完整度"""
        # 计算各维度得分
        basic_score = self._calculate_basic_dimension(user)
        experience_score = self._calculate_experience_dimension(user)
        capability_score = self._calculate_capability_dimension(user)
        achievement_score = self._calculate_achievement_dimension(user)
        content_score = self._calculate_content_professionalism(user)
        
        # 计算总分
        dimension_scores = {
            'basic_dimension': {
                'score': basic_score['score'],
                'weight': 0.4,
                'weighted_score': basic_score['score'] * 0.4
            },
            'experience_dimension': {
                'score': experience_score['score'],
                'weight': 0.3,
                'weighted_score': experience_score['score'] * 0.3
            },
            'capability_dimension': {
                'score': capability_score['score'],
                'weight': 0.2,
                'weighted_score': capability_score['score'] * 0.2
            },
            'achievement_dimension': {
                'score': achievement_score['score'],
                'weight': 0.1,
                'weighted_score': achievement_score['score'] * 0.1
            }
        }
        
        total_score = sum(item['weighted_score'] for item in dimension_scores.values())
        
        return {
            'total_score': int(total_score),
            'total_detail': dimension_scores,  # 添加总分明细
            'level': self._calculate_level(total_score),
            'basic_dimension': basic_score,
            'experience_dimension': experience_score,
            'capability_dimension': capability_score,
            'achievement_dimension': achievement_score,
            'content_professionalism': content_score,
            'improvement_suggestions': self._generate_improvement_suggestions(user)
        }
    
    def _calculate_basic_dimension(self, user):
        """计算基础维度得分"""
        details = {
            'basic_info': self._check_basic_info(user),
            'job_intention': self._check_job_intention(user),
            'education': self._check_education(user),
            'skills': self._check_skills(user)
        }
        score = sum(details.values())
        return {
            'score': score,
            'weight': 0.4,
            'weighted_score': score * 0.4,
            'details': details
        }
    
    def _check_basic_info(self, user):
        """检查基本信息完整度"""
        score = 0
        basic_info = getattr(user, 'basic_info', None)
        if basic_info:
            if basic_info.avatar:
                score += 5
            if basic_info.name:
                score += 5
            if all([basic_info.gender, basic_info.birthday, basic_info.location]):
                score += 6
            if basic_info.bio:
                score += 4
        return score
    
    def _generate_improvement_suggestions(self, user, *scores):
        """生成改进建议"""
        suggestions = []
        
        # 基本信息建议
        basic_info = getattr(user, 'basic_info', None)
        if not basic_info or not basic_info.avatar:
            suggestions.append({
                'type': 'basic_info',
                'field': 'avatar',
                'importance': 'high',
                'message': '添加头像可以让你的档案更加专业',
                'score_impact': 5
            })
        
        # 工作经验建议
        work_count = user.work_experiences.count()
        if work_count == 0:
            suggestions.append({
                'type': 'work_experience',
                'field': 'general',
                'importance': 'high',
                'message': '添加工作经历可以展示你的职业发展轨迹',
                'score_impact': 10
            })
        elif work_count == 1:
            suggestions.append({
                'type': 'work_experience',
                'field': 'detail',
                'importance': 'medium',
                'message': '完善工作经历的具体描述，突出你的职责和成果',
                'score_impact': 5
            })
            
        # 技能建议
        skills = user.skills.all()
        if not skills.exists():
            suggestions.append({
                'type': 'skills',
                'field': 'general',
                'importance': 'high',
                'message': '添加技能特长可以突出你的专业优势',
                'score_impact': 8
            })
            
        # 项目经验建议
        projects = user.projects.all()
        if not projects.exists():
            suggestions.append({
                'type': 'projects',
                'field': 'general',
                'importance': 'medium',
                'message': '添加项目经历可以展示你的实践能力',
                'score_impact': 6
            })
            
        return suggestions 
    
    def _check_job_intention(self, user):
        """检查求职意向完整度"""
        score = 0
        job_intention = getattr(user, 'job_intention', None)
        if job_intention:
            if job_intention.job_type:
                score += 3
            if job_intention.expected_salary:
                score += 3
            if job_intention.expected_city:
                score += 3
            if job_intention.job_status:
                score += 3
            if job_intention.description:
                score += 3
        return score
    
    def _check_education(self, user):
        """检查教育经历完整度"""
        score = 0
        educations = user.educations.all()
        if educations:
            # 基础分：有教育经历
            score += 5
            # 完整性加分
            for edu in educations[:3]:  # 最多计算3条
                if all([edu.school, edu.major, edu.degree, edu.start_date]):
                    score += 5
        return min(score, 15)  # 最高15分
    
    def _check_skills(self, user):
        """检查技能特长完整度"""
        score = 0
        skills = user.skills.all()
        if skills:
            for skill in skills[:5]:  # 最多计算5个技能
                if skill.name and skill.level:
                    score += 2
        return min(score, 10)  # 最高10分
    
    def _calculate_experience_dimension(self, user):
        """计算经验维度得分"""
        details = {
            'work_experience': self._check_work_experience(user),
            'project_experience': self._check_project_experience(user),
            'internship': self._check_internship(user)
        }
        score = sum(details.values())
        return {
            'score': score,
            'weight': 0.3,
            'weighted_score': score * 0.3,
            'details': details
        }
    
    def _check_work_experience(self, user):
        """检查工作经验完整度"""
        score = 0
        experiences = user.work_experiences.all()
        if experiences:
            # 基础分：有工作经验
            score += 5
            # 完整性加分
            for exp in experiences[:3]:  # 最多计算3份工作经验
                if all([exp.company, exp.position, exp.start_date, exp.description]):
                    score += 5
        return min(score, 15)  # 最高15分
    
    def _check_project_experience(self, user):
        """检查项目经验完整度"""
        score = 0
        projects = user.projects.all()
        if projects:
            for proj in projects[:2]:  # 最多计算2个项目
                if all([proj.name, proj.role, proj.description]):
                    score += 5
        return min(score, 10)  # 最高10分
    
    def _check_internship(self, user):
        """检查实习经验完整度"""
        score = 0
        internships = user.work_experiences.filter(is_internship=True)
        if internships:
            for intern in internships[:2]:  # 最多计算2段实习经历
                if all([intern.company, intern.position, intern.description]):
                    score += 2.5
        return min(score, 5)  # 最高5分
    
    def _calculate_level(self, score):
        """根据分数计算等级"""
        if score >= 90:
            return 'excellent'
        elif score >= 80:
            return 'good'
        elif score >= 70:
            return 'qualified'
        else:
            return 'improving'
    
    def _calculate_content_professionalism(self, user):
        """计算文字专业度"""
        work_scores = {
            'responsibility': self._check_work_content(user),
            'achievement': self._check_work_achievement(user),
            'keywords': self._check_work_keywords(user)
        }
        
        project_scores = {
            'background': self._check_project_content(user),
            'contribution': self._check_project_contribution(user),
            'result': self._check_project_result(user)
        }
        
        details = {
            'work_description': sum(work_scores.values()),
            'project_description': sum(project_scores.values())
        }
        score = sum(details.values())
        
        return {
            'score': score,
            'weight': 0.0,  # 文字专业度暂不计入总分
            'weighted_score': 0.0,
            'details': details
        }
    
    def _check_work_content(self, user):
        """检查工作描述内容"""
        return 3  # 暂时返回固定分数
    
    def _check_work_achievement(self, user):
        """检查工作成果描述"""
        return 2  # 暂时返回固定分数
    
    def _check_work_keywords(self, user):
        """检查工作关键词"""
        return 4  # 暂时返回固定分数
    
    def _check_project_content(self, user):
        """检查项目描述内容"""
        return 3  # 暂时返回固定分数
    
    def _check_project_contribution(self, user):
        """检查项目贡献描述"""
        return 2  # 暂时返回固定分数
    
    def _check_project_result(self, user):
        """检查项目结果描述"""
        return 3  # 暂时返回固定分数
    
    def _calculate_capability_dimension(self, user):
        """计算能力维度得分"""
        details = {
            'skill_relevance': self._check_skill_relevance(user),
            'certification': self._check_certification(user),
            'language': self._check_language(user)
        }
        score = sum(details.values())
        return {
            'score': score,
            'weight': 0.2,
            'weighted_score': score * 0.2,
            'details': details
        }
    
    def _check_skill_relevance(self, user):
        """检查技能相关度"""
        score = 0
        skills = user.skills.all()
        if skills:
            # 基础分：有技能记录
            score += 4
            # 技能描述完整性
            for skill in skills[:4]:  # 最多计算4个技能
                if skill.description:
                    score += 1
        return min(score, 8)  # 最高8分
    
    def _check_certification(self, user):
        """检查证书认证"""
        score = 0
        certificates = user.certificates.all()
        if certificates:
            for cert in certificates[:2]:  # 最多计算2个证书
                if all([cert.name, cert.issuing_authority, cert.issue_date]):
                    score += 2
        return min(score, 4)  # 最高4分
    
    def _check_language(self, user):
        """检查语言能力"""
        score = 0
        languages = user.languages.all()
        if languages:
            for lang in languages[:2]:  # 最多计算2种语言
                if all([lang.name, lang.level]):
                    score += 2
        return min(score, 4)  # 最高4分
    
    def _calculate_achievement_dimension(self, user):
        """计算成就维度得分"""
        details = {
            'awards': self._check_awards(user),
            'publications': self._check_publications(user),
            'portfolio': self._check_portfolio(user)
        }
        score = sum(details.values())
        return {
            'score': score,
            'weight': 0.1,
            'weighted_score': score * 0.1,
            'details': details
        }
    
    def _check_awards(self, user):
        """检查获奖情况"""
        score = 0
        certificates = user.certificates.filter(type='award')
        if certificates:
            for cert in certificates[:2]:
                if cert.description:
                    score += 1
        return min(score, 2)  # 最高2分
    
    def _check_publications(self, user):
        """检查发表作品"""
        # 这里可以根据实际需求扩展
        return 0
    
    def _check_portfolio(self, user):
        """检查作品集"""
        score = 0
        portfolios = user.portfolios.all()
        if portfolios:
            for portfolio in portfolios[:4]:  # 最多计算4个作品
                if all([portfolio.title, portfolio.description]):
                    score += 1
        return min(score, 4)  # 最高4分 