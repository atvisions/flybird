from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from users.models import User

class Question(models.Model):
    """问题"""
    STATUS_CHOICES = [
        ('open', '未解决'),
        ('closed', '已解决'),
    ]

    title = models.CharField(_('标题'), max_length=200)
    content = CKEditor5Field(_('内容'), config_name='default')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('提问者')
    )
    tags = models.CharField(_('标签'), max_length=200, blank=True, help_text='多个标签用逗号分隔')
    status = models.CharField(
        _('状态'),
        max_length=10,
        choices=STATUS_CHOICES,
        default='open'
    )
    views = models.PositiveIntegerField(_('浏览量'), default=0)
    likes = models.PositiveIntegerField(_('点赞数'), default=0)
    accepted_answer = models.OneToOneField(
        'Answer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_for',
        verbose_name=_('采纳的答案')
    )
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('问题')
        verbose_name_plural = _('问题')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Answer(models.Model):
    """答案"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_('问题')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_('回答者')
    )
    content = CKEditor5Field(_('内容'), config_name='default')
    likes = models.PositiveIntegerField(_('点赞数'), default=0)
    is_accepted = models.BooleanField(_('是否被采纳'), default=False)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('答案')
        verbose_name_plural = _('答案')
        ordering = ['-likes', '-created_at']

    def __str__(self):
        return f'Answer to: {self.question.title}'

class Comment(models.Model):
    """评论"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True,
        verbose_name=_('问题')
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True,
        verbose_name=_('答案')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='qa_comments',
        verbose_name=_('评论者')
    )
    content = models.TextField(_('内容'))
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('评论')
        verbose_name_plural = _('评论')
        ordering = ['created_at'] 