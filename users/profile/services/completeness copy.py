from typing import Dict, List
from users.profile.models import WorkExperience, Education, Skill, Language, Certificate, Portfolio, ProfileLayout
from users.models import ProfileScore  # 只从 users.models 导入
import logging


logger = logging.getLogger(__name__)

class CompletenessCalculator:
    """档案完整度评分服务"""
    
    LEVELS = {
        'expert': {'name': '专家用户', 'min_score': 85},
        'excellent': {'name': '优秀用户', 'min_score': 70},
        'improving': {'name': '成长用户', 'min_score': 0}
    }
    
    def __init__(self, user):
        self.user = user
        # 确保 profile_score 存在
        self.score, created = ProfileScore.objects.get_or_create(user=user)
        
    def get_completeness(self) -> Dict:
        """获取档案完整度评分"""
        total_score = self.score.total_score
        
        return {
            'code': 200,
            'message': '获取成功',
            'data': {
                'total_score': round(total_score, 1),
                'total_detail': {
                    'basic_dimension': {
                        'score': float(self.score.basic_dimension),
                        'weight': 0.4,
                        'weighted_score': round(self.score.basic_dimension * 0.4, 1)
                    },
                    'experience_dimension': {
                        'score': float(self.score.experience_dimension),
                        'weight': 0.3,
                        'weighted_score': round(self.score.experience_dimension * 0.3, 1)
                    },
                    'capability_dimension': {
                        'score': float(self.score.ability_dimension),
                        'weight': 0.2,
                        'weighted_score': round(self.score.ability_dimension * 0.2, 1)
                    },
                    'achievement_dimension': {
                        'score': float(self.score.achievement_dimension),
                        'weight': 0.1,
                        'weighted_score': round(self.score.achievement_dimension * 0.1, 1)
                    }
                },
                'level': self.get_user_level(total_score),
                'basic_dimension': {
                    'score': float(self.score.basic_dimension),
                    'weight': 0.4,
                    'weighted_score': round(self.score.basic_dimension * 0.4, 1)
                },
                'experience_dimension': {
                    'score': float(self.score.experience_dimension),
                    'weight': 0.3,
                    'weighted_score': round(self.score.experience_dimension * 0.3, 1)
                },
                'capability_dimension': {
                    'score': float(self.score.ability_dimension),
                    'weight': 0.2,
                    'weighted_score': round(self.score.ability_dimension * 0.2, 1)
                },
                'achievement_dimension': {
                    'score': float(self.score.achievement_dimension),
                    'weight': 0.1,
                    'weighted_score': round(self.score.achievement_dimension * 0.1, 1)
                },
                'content_professionalism': {
                    'score': round(total_score, 1),
                    'weight': 0.0,
                    'weighted_score': 0.0
                },
                'improvement_suggestions': self.get_improvement_suggestions()
            }
        }
        
    def get_user_level(self, total_score: float) -> str:
        """获取用户等级"""
        for level, info in self.LEVELS.items():
            if total_score >= info['min_score']:
                return level
        return 'improving'
        
    def get_improvement_suggestions(self) -> List[Dict]:
        """获取优化建议"""
        suggestions = []
        basic_info = self.user.basic_info
        
        # 基础维度建议
        if not basic_info.avatar:
            suggestions.append({
                'type': 'basic_info',
                'field': 'avatar',
                'importance': 'high',
                'message': '添加头像可以让你的档案加专业',
                'score_impact': 20
            })
        
        if not basic_info.personal_summary:
            suggestions.append({
                'type': 'basic_info',
                'field': 'personal_summary',
                'importance': 'high',
                'message': '添加个人简介可以让招聘方更好地了解你',
                'score_impact': 15
            })
        elif len(basic_info.personal_summary) < 100:
            suggestions.append({
                'type': 'basic_info',
                'field': 'personal_summary',
                'importance': 'medium',
                'message': '完善个人简介至100字以上可以获得更高评分',
                'score_impact': 10
            })
        
        # 经验维度建议
        work_count = WorkExperience.objects.filter(user=self.user).count()
        if work_count == 0:
            suggestions.append({
                'type': 'work_experience',
                'field': 'work_experience',
                'importance': 'high',
                'message': '添加工作经历可以展示你的职业发展',
                'score_impact': 20
            })
        elif work_count < 3:
            suggestions.append({
                'type': 'work_experience',
                'field': 'work_experience',
                'importance': 'medium',
                'message': f'再添加{3-work_count}段工作经历可以获得满分',
                'score_impact': (3-work_count) * 20
            })
        
        # 能力维度建议
        skill_count = Skill.objects.filter(user=self.user).count()
        if skill_count == 0:
            suggestions.append({
                'type': 'skill',
                'field': 'skill',
                'importance': 'high',
                'message': '添加技能特长可以突出你的专业能力',
                'score_impact': 12
            })
        elif skill_count < 5:
            suggestions.append({
                'type': 'skill',
                'field': 'skill',
                'importance': 'medium',
                'message': f'再添加{5-skill_count}个技能可以获得满分',
                'score_impact': (5-skill_count) * 12
            })
        
        # 成就维度建议
        cert_count = Certificate.objects.filter(user=self.user).count()
        port_count = Portfolio.objects.filter(user=self.user).count()
        
        if cert_count == 0:
            suggestions.append({
                'type': 'certificate',
                'field': 'certificate',
                'importance': 'medium',
                'message': '添加专业证书以证明你的能力水平',
                'score_impact': 25
            })
        
        if port_count == 0:
            suggestions.append({
                'type': 'portfolio',
                'field': 'portfolio',
                'importance': 'medium',
                'message': '添加作品集可以展示你的实际项目经验',
                'score_impact': 20
            })
        
        return suggestions 
        
    def get_content_quality_status(self) -> Dict:
        """获取内容质量状态"""
        try:
            # 计算各维度得分
            basic_score = self.calculate_basic_score()
            experience_score = self.calculate_experience_score()
            capability_score = self.calculate_capability_score()
            achievement_score = self.calculate_achievement_score()
            
            # 计算总分
            total_score = (
                basic_score * 0.4 +
                experience_score * 0.3 +
                capability_score * 0.2 +
                achievement_score * 0.1
            )
            
            # 更新数据库中的分数
            self.score.basic_dimension = basic_score
            self.score.experience_dimension = experience_score
            self.score.ability_dimension = capability_score
            self.score.achievement_dimension = achievement_score
            self.score.total_score = total_score
            self.score.save()
            
            return {
                'code': 200,
                'message': '获取成功',
                'data': {
                    'total_score': round(total_score, 1),
                    'dimensions': {
                        'basic_info': {
                            'score': float(basic_score),
                            'weight': 0.4,
                            'weighted_score': round(basic_score * 0.4, 1)
                        },
                        'experience': {
                            'score': float(experience_score),
                            'weight': 0.3,
                            'weighted_score': round(experience_score * 0.3, 1)
                        },
                        'capability': {
                            'score': float(capability_score),
                            'weight': 0.2,
                            'weighted_score': round(capability_score * 0.2, 1)
                        },
                        'achievement': {
                            'score': float(achievement_score),
                            'weight': 0.1,
                            'weighted_score': round(achievement_score * 0.1, 1)
                        }
                    },
                    'suggestions': self.get_improvement_suggestions()
                }
            }
        except Exception as e:
            logger.error(f"获取内容质量状态失败: {str(e)}")
            return {
                'code': 500,
                'message': str(e),
                'data': None
            }

    def calculate_basic_score(self) -> float:
        """计算基础维度得分"""
        try:
            score = 0
            basic_info = self.user.basic_info
            
            # 头像 20分
            if basic_info.avatar:
                score += 20
            
            # 个人简介 20分
            if basic_info.personal_summary:
                if len(basic_info.personal_summary) >= 100:
                    score += 20
                else:
                    score += 10
            
            # 其他基本信息 30分
            if basic_info.name:
                score += 10
            if basic_info.gender:
                score += 5
            if hasattr(basic_info, 'birth_date') and basic_info.birth_date:
                score += 5
            if basic_info.phone:
                score += 5
            if basic_info.email:
                score += 5
            
            return score
        except Exception as e:
            logger.error(f"计算基础维度得分失败: {str(e)}")
            return 0.0

    def calculate_experience_score(self) -> float:
        """计算经验维度得分"""
        score = 0
        
        # 工作经历 60分
        work_count = WorkExperience.objects.filter(user=self.user).count()
        score += min(work_count * 20, 60)
        
        # 教育经历 40分
        education_count = Education.objects.filter(user=self.user).count()
        score += min(education_count * 20, 40)
        
        return score

    def calculate_capability_score(self) -> float:
        """计算能力维度得分"""
        score = 0
        
        # 技能特长 60分
        skill_count = Skill.objects.filter(user=self.user).count()
        score += min(skill_count * 12, 60)
        
        # 语言能力 40分
        language_count = Language.objects.filter(user=self.user).count()
        score += min(language_count * 20, 40)
        
        return score

    def calculate_achievement_score(self) -> float:
        """计算成就维度得分"""
        score = 0
        
        # 证书 50分
        cert_count = Certificate.objects.filter(user=self.user).count()
        score += min(cert_count * 25, 50)
        
        # 作品集 50分
        port_count = Portfolio.objects.filter(user=self.user).count()
        score += min(port_count * 25, 50)
        
        return score 