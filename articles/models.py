from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from users.models import User

class Category(models.Model):
    """文章分类"""
    name = models.CharField(_('分类名称'), max_length=50)
    slug = models.SlugField(_('分类标识'), unique=True)
    description = models.TextField(_('分类描述'), blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('分类')
        verbose_name_plural = _('分类')
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):
    """文章"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    title = models.CharField(_('标题'), max_length=200)
    slug = models.SlugField(_('URL标识'), unique=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name=_('作者')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        verbose_name=_('分类')
    )
    cover = models.ImageField(_('封面图'), upload_to='articles/covers/%Y/%m/', blank=True)
    summary = models.TextField(_('摘要'), blank=True)
    content = CKEditor5Field(_('内容'), config_name='default')
    status = models.CharField(
        _('状态'),
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    views = models.PositiveIntegerField(_('浏览量'), default=0)
    likes = models.PositiveIntegerField(_('点赞数'), default=0)
    is_featured = models.BooleanField(_('是否推荐'), default=False)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    published_at = models.DateTimeField(_('发布时间'), null=True, blank=True)

    class Meta:
        verbose_name = _('文章')
        verbose_name_plural = _('文章')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    """评论"""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('文章')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('作者')
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name=_('父评论')
    )
    content = models.TextField(_('内容'))
    is_public = models.BooleanField(_('是否公开'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('评论')
        verbose_name_plural = _('评论')
        ordering = ['-created_at'] 