from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class JobIntention(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='job_intention'
    )
    job_type = models.CharField(max_length=50, blank=True)
    job_status = models.CharField(max_length=50, blank=True)
    expected_salary = models.CharField(max_length=50, blank=True)
    expected_city = models.CharField(max_length=100, blank=True)
    industries = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(
        '创建时间',
        default=timezone.now
    )
    updated_at = models.DateTimeField(
        '更新时间',
        auto_now=True
    )

    class Meta:
        db_table = 'user_job_intention'
        verbose_name = '求职意向'
        verbose_name_plural = '求职意向'

    def __str__(self):
        return f"{self.user.username}'s job intention" 