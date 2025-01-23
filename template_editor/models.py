# template_editor/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """模版分类"""
    name = models.CharField(_('分类名称'), max_length=50)
    description = models.TextField(_('分类描述'), blank=True)
    sort_order = models.IntegerField(_('排序'), default=0)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('模版分类')
        verbose_name_plural = _('模版分类')
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name

class Template(models.Model):
    """简历模版"""
    STATUS_CHOICES = (
        (0, _('草稿')),
        (1, _('已发布')),
        (2, _('待审核')),
        (3, _('已下架')),
    )

    # 基本信息
    name = models.CharField(_('模版名称'), max_length=100)
    description = models.TextField(_('模版描述'), blank=True)
    thumbnail = models.ImageField(_('缩略图'), upload_to='templates/thumbnails/', blank=True)
    category = models.ForeignKey(Category, verbose_name=_('所属分类'), 
                                on_delete=models.SET_NULL, null=True)
    keywords = models.JSONField(_('关键词'), default=list)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('创建者'),
                               on_delete=models.CASCADE)
    is_public = models.BooleanField(_('是否公开'), default=False)
    status = models.SmallIntegerField(_('状态'), choices=STATUS_CHOICES, default=0)
    is_recommended = models.BooleanField(_('是否推荐'), default=False, help_text=_('设置为推荐模板'))
    
    # 画布数据 - 使用 JSONField 存储多页画布数据
    pages = models.JSONField(_('画布页面'), default=list, help_text=_('存储多个画布页面的数据'))
    
    # 时间信息
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    # 统计字段
    views = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    likes = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    liked_by = models.ManyToManyField(
        'users.User',
        related_name='liked_templates',
        blank=True,
        verbose_name='点赞用户'
    )

    class Meta:
        verbose_name = _('简历模版')
        verbose_name_plural = _('简历模版')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_page_count(self):
        """获取页面数量"""
        return len(self.pages)

    def add_page(self):
        """添加新页面"""
        if self.get_page_count() >= 5:
            raise ValueError(_('最多只能创建5个页面'))
        
        # 创建新页面
        new_page = {
            'config': {
                'width': 794,        # A4纸宽度（像素）
                'height': 1123,      # A4纸高度（像素）
                'backgroundColor': '#ffffff',
                'showGrid': True,
                'gridSize': 10,
                'gridColor': '#f0f0f0',
                'showGuideLine': True
            },
            'elements': []  # 初始化空元素列表
        }
        
        self.pages.append(new_page)
        self.save()
        return len(self.pages) - 1  # 返回新页面的索引

    def update_page(self, page_index, page_data):
        """更新指定页面"""
        if not 0 <= page_index < len(self.pages):
            raise ValueError(_('无效的页面索引'))
        
        self.pages[page_index] = page_data
        self.save()

    def delete_page(self, page_index):
        """删除指定页面"""
        if page_index == 0:
            raise ValueError(_('不能删除第一页'))
        
        if not 0 <= page_index < len(self.pages):
            raise ValueError(_('无效的页面索引'))
        
        self.pages.pop(page_index)
        self.save()