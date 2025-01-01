# users/profile/models/layout.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class ProfileLayout(models.Model):
    """档案布局"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_layout'
    )
    layout = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    DEFAULT_LAYOUT = {
        'job_intention': {'order': 1, 'visible': True},
        'work_experience': {'order': 2, 'visible': True},
        'education': {'order': 3, 'visible': False},
        'project': {'order': 4, 'visible': False},
        'skill': {'order': 5, 'visible': False},
        'certificate': {'order': 6, 'visible': False},
        'language': {'order': 7, 'visible': False},
        'portfolio': {'order': 8, 'visible': False},
        'social_link': {'order': 9, 'visible': False}
    }

    def save(self, *args, **kwargs):
        if not self.pk and not self.layout:
            self.layout = self.DEFAULT_LAYOUT.copy()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '档案布局'
        verbose_name_plural = verbose_name