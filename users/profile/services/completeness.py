from typing import Dict, List
from users.profile.models import WorkExperience, Education, Skill, Language, Certificate, Portfolio, ProfileScore, Project

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
        
        # 构建内容质量数据
        content_quality_data = {
            'score': float(self.score.content_quality),
            'weight': 0.0,  # 预留权重
            'weighted_score': 0.0,
            'status': self.get_content_quality_status(),
            'can_optimize': True,
            'optimize_fields': self.get_optimize_fields(),  # 添加可优化的字段列表
            'optimized_fields': self.score.optimized_fields or []  # 添加已优化字段列表
        }
        
        # 获取可优化字段，但排除已优化的
        optimize_fields = self.get_optimize_fields()
        if self.score.optimized_fields:
            optimize_fields = [
                field for field in optimize_fields 
                if field['field'] not in self.score.optimized_fields
            ]
        
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
                    },
                    'content_quality': content_quality_data
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
                'content_quality': content_quality_data,
                'improvement_suggestions': self.get_improvement_suggestions(optimize_fields)
            }
        }
        
    def get_user_level(self, total_score: float) -> str:
        """获取用户等级"""
        for level, info in self.LEVELS.items():
            if total_score >= info['min_score']:
                return level
        return 'improving'
        
    def get_content_quality_status(self) -> str:
        """获取内容质量状态"""
        if self.score.content_quality >= 8:
            return 'excellent'
        elif self.score.content_quality >= 6:
            return 'good'
        elif self.score.content_quality > 0:
            return 'improving'
        return 'pending'
        
    def get_optimize_fields(self) -> List[Dict]:
        """获取可优化的字段列表"""
        fields = []
        basic_info = self.user.basic_info
        
        # 检查个人简介
        if basic_info.personal_summary:
            fields.append({
                'field': 'personal_summary',
                'name': '个人简介',
                'current_length': len(basic_info.personal_summary),
                'can_optimize': True
            })
        
        # 检查工作经历描述
        work_experiences = WorkExperience.objects.filter(user=self.user)
        for work in work_experiences:
            if work.description:
                fields.append({
                    'field': f'work_experience_{work.id}',
                    'name': f'工作经历 - {work.company}',
                    'current_length': len(work.description),
                    'can_optimize': True
                })
        
        # 检查项目经历描述
        projects = Project.objects.filter(user=self.user)
        for project in projects:
            if project.description or project.achievement:
                fields.append({
                    'field': f'project_{project.id}',
                    'name': f'项目经历 - {project.name}',
                    'current_length': len(project.description or '') + len(project.achievement or ''),
                    'can_optimize': True
                })
        
        return fields
        
    def get_improvement_suggestions(self, optimize_fields=None) -> List[Dict]:
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
        
        # 内容质量建议
        if optimize_fields:  # 只有还有未优化的字段时才添加建议
            suggestions.append({
                'type': 'content',
                'field': 'content_quality',
                'importance': 'medium',
                'message': '使用AI助手优化您的文字表达，提升专业度',
                'score_impact': 10,
                'can_optimize': True,
                'optimize_fields': optimize_fields,
                'optimize_tips': [
                    '使用更专业的词汇和表达方式',
                    '突出关键成就和数据',
                    '保持逻辑性和连贯性',
                    '适当增加行业术语'
                ]
            })
        
        return suggestions 