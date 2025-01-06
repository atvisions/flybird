from django.db import models
from django.conf import settings

class Portfolio(models.Model):
    """作品集"""
    TYPE_CHOICES = [
        ('project', '项目'),
        ('website', '网站'),
        ('app', '应用'),
        ('article', '文章'),
        ('other', '其他')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolios',
        verbose_name='用户'
    )
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='标题')
    type = models.CharField(
        '作品类型',
        max_length=20,
        choices=TYPE_CHOICES,
        default='project'
    )
    description = models.TextField('作品描述', blank=True)
    url = models.URLField('作品链接', blank=True)
    image = models.ImageField('作品图片', upload_to='portfolios/', blank=True)
    highlights = models.TextField('项目亮点', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    order = models.IntegerField(default=0, verbose_name='排序')
    class Meta:
        verbose_name = '作品集'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.phone} 的作品: {self.title}' 