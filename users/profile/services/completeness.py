from typing import Dict, List
from users.profile.models import WorkExperience, Education, Skill, Language, Certificate, Portfolio, ProfileScore

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
                'message': '添加头像可以让你的档案更加专业',
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
                'message': '添加专业证书可以证明你的能力水平',
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