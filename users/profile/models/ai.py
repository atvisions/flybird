from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AIOptimizationSuggestion(models.Model):
    """AI优化建议模型"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('adopted', '已采纳'),
        ('rejected', '已拒绝'),
    ]
    
    FIELD_CHOICES = [
        ('personal_summary', '个人简介'),
        ('work_experience', '工作经历'),
        ('skill', '技能特长'),
        ('education', '教育经历'),
        ('project', '项目经验'),
        ('certificate', '证书奖项'),
        ('portfolio', '作品集'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='ai_suggestions',
        verbose_name='用户'
    )
    field = models.CharField('优化字段', max_length=50, choices=FIELD_CHOICES)
    original_content = models.TextField('原始内容')
    suggested_content = models.TextField('建议内容')
    reason = models.TextField('优化理由')
    status = models.CharField(
        '处理状态',
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user_ai_suggestion'
        verbose_name = 'AI优化建议'
        verbose_name_plural = 'AI优化建议'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.field} 优化建议"

class AIQualityImprovement(models.Model):
    """AI质量改进记录模型"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='ai_improvements',
        verbose_name='用户'
    )
    field = models.CharField('改进字段', max_length=50)
    original_content = models.TextField('原始内容')
    improved_content = models.TextField('改进后内容')
    improvement_score = models.FloatField('改进分数')  # 改进幅度评分 (0-100)
    improvement_details = models.JSONField('改进详情', default=dict)  # 存储详细的改进点
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'user_ai_improvement'
        verbose_name = 'AI质量改进记录'
        verbose_name_plural = 'AI质量改进记录'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.field} 质量改进"

class AIOptimizationQuota(models.Model):
    """AI优化次数配额模型"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='ai_quota',
        verbose_name='用户'
    )
    total_quota = models.IntegerField('总配额', default=3)  # 每月总配额
    used_quota = models.IntegerField('已使用次数', default=0)
    reset_date = models.DateField('重置日期')  # 下次重置配额的日期
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user_ai_quota'
        verbose_name = 'AI优化配额'
        verbose_name_plural = 'AI优化配额'

    def __str__(self):
        return f"{self.user.username} 的AI优化配额"

    @property
    def remaining_quota(self):
        """剩余配额"""
        return max(0, self.total_quota - self.used_quota) 