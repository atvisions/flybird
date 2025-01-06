from django.db import models
from django.conf import settings
from django.utils import timezone

class ProfileLayout(models.Model):
    """档案布局"""
    DEFAULT_LAYOUT = {
        'basic_info': {'order': 1, 'visible': True},
        'job_intention': {'order': 2, 'visible': True},
        'work_experience': {'order': 3, 'visible': True},
        'education': {'order': 4, 'visible': False},
        'project': {'order': 5, 'visible': False},
        'skill': {'order': 6, 'visible': False},
        'certificate': {'order': 7, 'visible': False},
        'language': {'order': 8, 'visible': False},
        'portfolio': {'order': 9, 'visible': False},
        'social_link': {'order': 10, 'visible': False}
    }

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_layout',
        unique=True
    )
    layout = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '档案布局'
        verbose_name_plural = verbose_name
        unique_together = ['user']

    def __str__(self):
        return f'{self.user.phone} 的档案布局'

    def save(self, *args, **kwargs):
        if not self.pk and not self.layout:
            self.layout = self.DEFAULT_LAYOUT.copy()
        super().save(*args, **kwargs)

    @property
    def total_score(self):
        """计算总分"""
        return (
            self.basic_dimension * 0.4 +
            self.experience_dimension * 0.3 +
            self.ability_dimension * 0.2 +
            self.achievement_dimension * 0.1
        ) 