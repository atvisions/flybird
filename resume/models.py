from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TemplateCategory(models.Model):
    """简历模板分类"""
    name = models.CharField('分类名称', max_length=50)
    icon = models.CharField('分类图标', max_length=50, blank=True)
    description = models.TextField('分类描述', blank=True)
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='children', verbose_name='父分类')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '模板分类'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name

class ComponentCategory(models.Model):
    """组件分类"""
    name = models.CharField('分类名称', max_length=50)
    code = models.CharField('分类编码', max_length=50, unique=True)
    icon = models.CharField('分类图标', max_length=50)
    description = models.TextField('分类描述', blank=True)
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '组件分类'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name

class Component(models.Model):
    """简历组件库"""
    TYPE_CHOICES = (
        ('text', '文本'),
        ('image', '图片'),
        ('list', '列表'),
        ('table', '表格'),
        ('timeline', '时间线'),
        ('title', '标题'),
        ('paragraph', '段落'),
        ('education', '教育经历'),
        ('experience', '工作经历'),
        ('skills', '技能列表'),
        ('contact', '联系方式'),
        ('projects', '项目经历'),
        ('awards', '获奖经历'),
        ('custom', '自定义组件'),
    )

    name = models.CharField('组件名称', max_length=50)
    type = models.CharField('组件类型', max_length=20, choices=TYPE_CHOICES)
    category = models.ForeignKey(ComponentCategory, on_delete=models.PROTECT, 
                                verbose_name='组件分类', related_name='components',
                                null=True, blank=True)
    icon = models.CharField('图标', max_length=50)
    description = models.TextField('组件描述', blank=True)
    preview_image = models.ImageField('预览图', upload_to='component_previews/', blank=True)
    config = models.JSONField('组件配置', help_text="""
    {
        "fields": [  # 组件包含的字段
            {
                "name": "字段名",
                "type": "字段类型(text/number/date/select/etc)",
                "label": "显示标签",
                "required": true/false,
                "default": "默认值",
                "options": ["选项1", "选项2"]  # 如果type是select
            }
        ],
        "styles": {  # 组件样式配置
            "width": "宽度",
            "margin": "外边距",
            "padding": "内边距",
            "font": "字体",
            "color": "颜色",
            "background": "背景"
        },
        "layout": {  # 组件布局配置
            "grid": "网格位置",
            "alignment": "对齐方式"
        }
    }
    """)
    template = models.TextField('组件模板', help_text='组件的HTML模板，支持变量插值')
    is_system = models.BooleanField('是否系统组件', default=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '简历组件'
        verbose_name_plural = verbose_name
        ordering = ['category', 'type', 'id']

    def __str__(self):
        return self.name

class ResumeTemplate(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )

    name = models.CharField('模板名称', max_length=100)
    thumbnail = models.ImageField('缩略图', upload_to='resume_templates/')
    description = models.TextField('描述')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_templates')
    category = models.ForeignKey(TemplateCategory, on_delete=models.SET_NULL, null=True, 
                              related_name='templates', verbose_name='模板分类')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    is_vip = models.BooleanField('是否VIP模板', default=False)
    content = models.JSONField('模板内容', default=dict, help_text='保存画布上的所有元素数据')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '简历模板'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Resume(models.Model):
    name = models.CharField('简历名称', max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True)
    content = models.JSONField('简历内容')
    is_public = models.BooleanField('是否公开', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '简历'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']

    def __str__(self):
        return self.name 