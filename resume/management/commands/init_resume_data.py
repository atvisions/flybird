from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resume.models import TemplateCategory, Component

User = get_user_model()

class Command(BaseCommand):
    help = '初始化简历模块的基础数据'

    def handle(self, *args, **kwargs):
        self.stdout.write('开始初始化简历模块数据...')
        
        # 创建根分类
        self.create_categories()
        # 创建基础组件
        self.create_components()
        self.create_demo_data()
        
        self.stdout.write(self.style.SUCCESS('数据初始化完成！'))

    def create_categories(self):
        # 创建主分类
        categories_data = [
            {
                'name': '求职简历',
                'icon': 'job',
                'description': '适用于求职应聘的简历模板',
                'sort_order': 1,
                'subcategories': [
                    {'name': '应届生简历', 'sort_order': 1},
                    {'name': '社会招聘简历', 'sort_order': 2},
                    {'name': '高级人才简历', 'sort_order': 3},
                ]
            },
            {
                'name': '创意简历',
                'icon': 'creative',
                'description': '独特创意风格的简历模板',
                'sort_order': 2,
                'subcategories': [
                    {'name': '设计师简历', 'sort_order': 1},
                    {'name': '艺术家简历', 'sort_order': 2},
                    {'name': '自由职业者简历', 'sort_order': 3},
                ]
            },
            {
                'name': '行业简历',
                'icon': 'industry',
                'description': '针对特定行业的专业简历模板',
                'sort_order': 3,
                'subcategories': [
                    {'name': 'IT互联网', 'sort_order': 1},
                    {'name': '金融银行', 'sort_order': 2},
                    {'name': '医疗卫生', 'sort_order': 3},
                    {'name': '教育培训', 'sort_order': 4},
                    {'name': '销售市场', 'sort_order': 5},
                ]
            },
            {
                'name': '简约简历',
                'icon': 'simple',
                'description': '简洁大方的简历模板',
                'sort_order': 4,
                'subcategories': [
                    {'name': '单页简历', 'sort_order': 1},
                    {'name': '双页简历', 'sort_order': 2},
                    {'name': '多页简历', 'sort_order': 3},
                ]
            },
        ]

        for category_data in categories_data:
            subcategories = category_data.pop('subcategories')
            parent = TemplateCategory.objects.create(**category_data)
            self.stdout.write(f'创建主分类: {parent.name}')
            
            for sub_data in subcategories:
                TemplateCategory.objects.create(parent=parent, **sub_data)
                self.stdout.write(f'  创建子分类: {sub_data["name"]}')

    def create_components(self):
        # 创建系统组件
        components_data = [
            # 内容组件 - 基本信息
            {
                'name': '基本信息',
                'type': 'contact',
                'category': 'content',
                'icon': 'user',
                'description': '展示基本的个人联系信息',
                'config': {
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'text',
                            'label': '姓名',
                            'required': True,
                        },
                        {
                            'name': 'avatar',
                            'type': 'image',
                            'label': '头像',
                            'required': False,
                        },
                        {
                            'name': 'gender',
                            'type': 'select',
                            'label': '性别',
                            'required': False,
                            'options': ['male', 'female', 'other'],
                            'option_labels': ['男', '女', '其他']
                        },
                        {
                            'name': 'birth_date',
                            'type': 'date',
                            'label': '出生日期',
                            'required': False,
                        },
                        {
                            'name': 'phone',
                            'type': 'text',
                            'label': '手机号码',
                            'required': True,
                        },
                        {
                            'name': 'email',
                            'type': 'email',
                            'label': '电子邮箱',
                            'required': True,
                        },
                        {
                            'name': 'location',
                            'type': 'text',
                            'label': '所在地',
                            'required': False,
                        },
                        {
                            'name': 'personal_summary',
                            'type': 'textarea',
                            'label': '个人简介',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="basic-info">
                    <div class="avatar">
                        {% if avatar %}
                        <img src="{{ avatar }}" alt="{{ name }}">
                        {% endif %}
                    </div>
                    <h2>{{ name }}</h2>
                    <div class="info-list">
                        {% if gender %}<p>性别：{{ gender }}</p>{% endif %}
                        {% if birth_date %}<p>出生日期：{{ birth_date }}</p>{% endif %}
                        <p>联系电话：{{ phone }}</p>
                        <p>电子邮箱：{{ email }}</p>
                        {% if location %}<p>所在地：{{ location }}</p>{% endif %}
                    </div>
                    {% if personal_summary %}
                    <div class="summary">
                        <h3>个人简介</h3>
                        <p>{{ personal_summary }}</p>
                    </div>
                    {% endif %}
                </div>
                '''
            },
            # 内容组件 - 求职意向
            {
                'name': '求职意向',
                'type': 'job_intention',
                'category': 'content',
                'icon': 'target',
                'description': '展示求职意向信息',
                'config': {
                    'fields': [
                        {
                            'name': 'job_type',
                            'type': 'text',
                            'label': '期望职位',
                            'required': True,
                        },
                        {
                            'name': 'job_status',
                            'type': 'select',
                            'label': '求职状态',
                            'required': True,
                            'options': ['在职考虑机会', '离职寻找机会', '应届毕业生']
                        },
                        {
                            'name': 'expected_salary',
                            'type': 'text',
                            'label': '期望薪资',
                            'required': True,
                        },
                        {
                            'name': 'expected_city',
                            'type': 'text',
                            'label': '期望城市',
                            'required': True,
                        },
                        {
                            'name': 'industries',
                            'type': 'text',
                            'label': '期望行业',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="job-intention">
                    <h3>求职意向</h3>
                    <div class="intention-list">
                        <p><strong>期望职位：</strong>{{ job_type }}</p>
                        <p><strong>求职状态：</strong>{{ job_status }}</p>
                        <p><strong>期望薪资：</strong>{{ expected_salary }}</p>
                        <p><strong>期望城市：</strong>{{ expected_city }}</p>
                        {% if industries %}<p><strong>期望行业：</strong>{{ industries }}</p>{% endif %}
                    </div>
                </div>
                '''
            },
            # 内容组件 - 工作经历
            {
                'name': '工作经历',
                'type': 'experience',
                'category': 'content',
                'icon': 'work',
                'description': '展示工作经验',
                'config': {
                    'fields': [
                        {
                            'name': 'company',
                            'type': 'text',
                            'label': '公司名称',
                            'required': True,
                        },
                        {
                            'name': 'position',
                            'type': 'text',
                            'label': '职位',
                            'required': True,
                        },
                        {
                            'name': 'department',
                            'type': 'text',
                            'label': '部门',
                            'required': False,
                        },
                        {
                            'name': 'start_date',
                            'type': 'date',
                            'label': '入职时间',
                            'required': True,
                        },
                        {
                            'name': 'end_date',
                            'type': 'date',
                            'label': '离职时间',
                            'required': False,
                        },
                        {
                            'name': 'is_current',
                            'type': 'boolean',
                            'label': '是否在职',
                            'required': False,
                        },
                        {
                            'name': 'description',
                            'type': 'textarea',
                            'label': '工作描述',
                            'required': True,
                            'min_length': 50,
                        },
                        {
                            'name': 'achievements',
                            'type': 'textarea',
                            'label': '工作成就',
                            'required': False,
                        },
                        {
                            'name': 'technologies',
                            'type': 'textarea',
                            'label': '技术栈',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="work-experience">
                    <div class="company-info">
                        <h3>{{ company }}</h3>
                        <p class="position">{{ position }}{% if department %} · {{ department }}{% endif %}</p>
                        <p class="time">{{ start_date }} - {% if is_current %}至今{% else %}{{ end_date }}{% endif %}</p>
                    </div>
                    <div class="description">{{ description }}</div>
                    {% if achievements %}
                    <div class="achievements">
                        <h4>工作成就</h4>
                        <p>{{ achievements }}</p>
                    </div>
                    {% endif %}
                    {% if technologies %}
                    <div class="technologies">
                        <h4>技术栈</h4>
                        <p>{{ technologies }}</p>
                    </div>
                    {% endif %}
                </div>
                '''
            },
            # 内容组件 - 教育经历
            {
                'name': '教育经历',
                'type': 'education',
                'category': 'content',
                'icon': 'education',
                'description': '展示教育背景',
                'config': {
                    'fields': [
                        {
                            'name': 'school',
                            'type': 'text',
                            'label': '学校名称',
                            'required': True,
                        },
                        {
                            'name': 'major',
                            'type': 'text',
                            'label': '专业',
                            'required': True,
                        },
                        {
                            'name': 'degree',
                            'type': 'select',
                            'label': '学历',
                            'required': True,
                            'options': ['high_school', 'junior_college', 'bachelor', 'master', 'doctor', 'other'],
                            'option_labels': ['高中', '大专', '本科', '硕士', '博士', '其他']
                        },
                        {
                            'name': 'start_date',
                            'type': 'date',
                            'label': '入学时间',
                            'required': True,
                        },
                        {
                            'name': 'end_date',
                            'type': 'date',
                            'label': '毕业时间',
                            'required': False,
                        },
                        {
                            'name': 'is_current',
                            'type': 'boolean',
                            'label': '是否在读',
                            'required': False,
                        },
                        {
                            'name': 'description',
                            'type': 'textarea',
                            'label': '在校经历',
                            'required': False,
                        },
                        {
                            'name': 'achievements',
                            'type': 'textarea',
                            'label': '在校成就',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="education">
                    <div class="school-info">
                        <h3>{{ school }}</h3>
                        <p class="major">{{ degree }} · {{ major }}</p>
                        <p class="time">{{ start_date }} - {% if is_current %}至今{% else %}{{ end_date }}{% endif %}</p>
                    </div>
                    {% if description %}
                    <div class="description">
                        <h4>在校经历</h4>
                        <p>{{ description }}</p>
                    </div>
                    {% endif %}
                    {% if achievements %}
                    <div class="achievements">
                        <h4>在校成就</h4>
                        <p>{{ achievements }}</p>
                    </div>
                    {% endif %}
                </div>
                '''
            },
            # 内容组件 - 技能特长
            {
                'name': '技能特长',
                'type': 'skills',
                'category': 'content',
                'icon': 'star',
                'description': '展示专业技能',
                'config': {
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'text',
                            'label': '技能名称',
                            'required': True,
                        },
                        {
                            'name': 'level',
                            'type': 'select',
                            'label': '熟练程度',
                            'required': True,
                            'options': ['初级', '中级', '高级', '专家'],
                        },
                        {
                            'name': 'description',
                            'type': 'textarea',
                            'label': '技能描述',
                            'required': False,
                        },
                        {
                            'name': 'projects',
                            'type': 'textarea',
                            'label': '相关项目',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="skill">
                    <div class="skill-header">
                        <h3>{{ name }}</h3>
                        <span class="level">{{ level }}</span>
                    </div>
                    {% if description %}
                    <div class="description">{{ description }}</div>
                    {% endif %}
                    {% if projects %}
                    <div class="projects">
                        <h4>相关项目</h4>
                        <p>{{ projects }}</p>
                    </div>
                    {% endif %}
                </div>
                '''
            },
            # 内容组件 - 语言能力
            {
                'name': '语言能力',
                'type': 'language',
                'category': 'content',
                'icon': 'language',
                'description': '展示语言能力',
                'config': {
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'text',
                            'label': '语言名称',
                            'required': True,
                        },
                        {
                            'name': 'proficiency',
                            'type': 'select',
                            'label': '熟练程度',
                            'required': True,
                            'options': ['elementary', 'intermediate', 'advanced', 'native'],
                            'option_labels': ['入门', '中级', '高级', '母语']
                        },
                        {
                            'name': 'certification',
                            'type': 'text',
                            'label': '语言证书',
                            'required': False,
                        },
                        {
                            'name': 'score',
                            'type': 'text',
                            'label': '考试分数',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="language">
                    <h3>{{ name }}</h3>
                    <p class="proficiency">{{ proficiency }}</p>
                    {% if certification %}
                    <p class="certification">证书：{{ certification }}</p>
                    {% endif %}
                    {% if score %}
                    <p class="score">分数：{{ score }}</p>
                    {% endif %}
                </div>
                '''
            },
            # 内容组件 - 项目经历
            {
                'name': '项目经历',
                'type': 'projects',
                'category': 'content',
                'icon': 'project',
                'description': '展示项目经验',
                'config': {
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'text',
                            'label': '项目名称',
                            'required': True,
                        },
                        {
                            'name': 'role',
                            'type': 'text',
                            'label': '担任角色',
                            'required': True,
                        },
                        {
                            'name': 'start_date',
                            'type': 'date',
                            'label': '开始时间',
                            'required': True,
                        },
                        {
                            'name': 'end_date',
                            'type': 'date',
                            'label': '结束时间',
                            'required': False,
                        },
                        {
                            'name': 'is_current',
                            'type': 'boolean',
                            'label': '是否进行中',
                            'required': False,
                        },
                        {
                            'name': 'description',
                            'type': 'textarea',
                            'label': '项目描述',
                            'required': True,
                        },
                        {
                            'name': 'achievement',
                            'type': 'textarea',
                            'label': '项目成果',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="project">
                    <div class="project-header">
                        <h3>{{ name }}</h3>
                        <p class="role">{{ role }}</p>
                        <p class="time">{{ start_date }} - {% if is_current %}至今{% else %}{{ end_date }}{% endif %}</p>
                    </div>
                    <div class="description">{{ description }}</div>
                    {% if achievement %}
                    <div class="achievement">
                        <h4>项目成果</h4>
                        <p>{{ achievement }}</p>
                    </div>
                    {% endif %}
                </div>
                '''
            },
            # 内容组件 - 作品集
            {
                'name': '作品集',
                'type': 'portfolio',
                'category': 'content',
                'icon': 'portfolio',
                'description': '展示个人作品',
                'config': {
                    'fields': [
                        {
                            'name': 'title',
                            'type': 'text',
                            'label': '作品标题',
                            'required': True,
                        },
                        {
                            'name': 'type',
                            'type': 'select',
                            'label': '作品类型',
                            'required': True,
                            'options': ['project', 'website', 'app', 'article', 'other'],
                            'option_labels': ['项目', '网站', '应用', '文章', '其他']
                        },
                        {
                            'name': 'description',
                            'type': 'textarea',
                            'label': '作品描述',
                            'required': False,
                        },
                        {
                            'name': 'url',
                            'type': 'url',
                            'label': '作品链接',
                            'required': False,
                        },
                        {
                            'name': 'image',
                            'type': 'image',
                            'label': '作品图片',
                            'required': False,
                        },
                        {
                            'name': 'highlights',
                            'type': 'textarea',
                            'label': '项目亮点',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="portfolio">
                    <div class="portfolio-header">
                        <h3>{{ title }}</h3>
                        <span class="type">{{ type }}</span>
                    </div>
                    {% if image %}
                    <div class="portfolio-image">
                        <img src="{{ image }}" alt="{{ title }}">
                    </div>
                    {% endif %}
                    {% if description %}
                    <div class="description">{{ description }}</div>
                    {% endif %}
                    {% if highlights %}
                    <div class="highlights">
                        <h4>项目亮点</h4>
                        <p>{{ highlights }}</p>
                    </div>
                    {% endif %}
                    {% if url %}
                    <div class="portfolio-link">
                        <a href="{{ url }}" target="_blank">查看作品</a>
                    </div>
                    {% endif %}
                </div>
                '''
            },
            # 内容组件 - 社交主页
            {
                'name': '社交主页',
                'type': 'social',
                'category': 'content',
                'icon': 'link',
                'description': '展示社交账号链接',
                'config': {
                    'fields': [
                        {
                            'name': 'platform',
                            'type': 'select',
                            'label': '平台名称',
                            'required': True,
                            'options': ['weibo', 'zhihu', 'zcool', 'douyin', 'bilibili', 'github', 'twitter', 'website', 'other'],
                            'option_labels': ['新浪微博', '知乎', '站酷', '抖音', 'Bilibili', 'GitHub', 'Twitter', '个人网站', '其他']
                        },
                        {
                            'name': 'url',
                            'type': 'url',
                            'label': '链接地址',
                            'required': True,
                        },
                        {
                            'name': 'description',
                            'type': 'textarea',
                            'label': '链接描述',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="social-link">
                    <a href="{{ url }}" target="_blank" class="platform-link">
                        <i class="icon-{{ platform }}"></i>
                        <span class="platform-name">{{ platform }}</span>
                    </a>
                    {% if description %}
                    <p class="description">{{ description }}</p>
                    {% endif %}
                </div>
                '''
            },
            # 内容组件 - 证书奖项
            {
                'name': '证书奖项',
                'type': 'certificate',
                'category': 'content',
                'icon': 'certificate',
                'description': '展示证书和奖项',
                'config': {
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'text',
                            'label': '证书名称',
                            'required': True,
                        },
                        {
                            'name': 'type',
                            'type': 'select',
                            'label': '证书类型',
                            'required': True,
                            'options': ['professional', 'award', 'language', 'other'],
                            'option_labels': ['专业证书', '获奖证书', '语言证书', '其他证书']
                        },
                        {
                            'name': 'issuing_authority',
                            'type': 'text',
                            'label': '发证机构',
                            'required': True,
                        },
                        {
                            'name': 'issue_date',
                            'type': 'date',
                            'label': '发证日期',
                            'required': True,
                        },
                        {
                            'name': 'expiry_date',
                            'type': 'date',
                            'label': '到期日期',
                            'required': False,
                        },
                        {
                            'name': 'credential_id',
                            'type': 'text',
                            'label': '证书编号',
                            'required': False,
                        },
                        {
                            'name': 'description',
                            'type': 'textarea',
                            'label': '证书描述',
                            'required': False,
                        }
                    ]
                },
                'template': '''
                <div class="certificate">
                    <div class="certificate-header">
                        <h3>{{ name }}</h3>
                        <span class="type">{{ type }}</span>
                    </div>
                    <div class="certificate-info">
                        <p class="authority">发证机构：{{ issuing_authority }}</p>
                        <p class="date">发证日期：{{ issue_date }}</p>
                        {% if expiry_date %}
                        <p class="expiry">到期日期：{{ expiry_date }}</p>
                        {% endif %}
                        {% if credential_id %}
                        <p class="id">证书编号：{{ credential_id }}</p>
                        {% endif %}
                    </div>
                    {% if description %}
                    <div class="description">{{ description }}</div>
                    {% endif %}
                </div>
                '''
            }
        ]

        for component_data in components_data:
            # 检查组件是否已存在
            component, created = Component.objects.get_or_create(
                name=component_data['name'],
                type=component_data['type'],
                defaults=component_data
            )
            if created:
                self.stdout.write(f'创建组件: {component_data["name"]}') 

    def create_demo_data(self):
        """创建组件演示数据"""
        demo_data = {
            'text': {
                'content': '这是一段示例文本内容，用于展示文本组件的效果。',
                'alignment': 'left',
                'color': '#333333',
                'font_size': '16px'
            },
            'title': {
                'content': '示例标题',
                'level': 'h2',
                'alignment': 'center',
                'color': '#000000'
            },
            'paragraph': {
                'content': '这是一个段落示例，展示了段落组件的基本样式和排版效果。段落可以包含多行文本，并且可以设置行高、缩进等样式属性。',
                'indent': '2em',
                'line_height': '1.6'
            },
            'image': {
                'src': 'https://example.com/sample-image.jpg',
                'alt': '示例图片',
                'width': '100%',
                'alignment': 'center'
            },
            'list': {
                'type': 'unordered',
                'items': [
                    '列表项目一',
                    '列表项目二',
                    '列表项目三',
                    '列表项目四'
                ]
            },
            'table': {
                'headers': ['表头一', '表头二', '表头三'],
                'rows': [
                    ['数据1-1', '数据1-2', '数据1-3'],
                    ['数据2-1', '数据2-2', '数据2-3'],
                    ['数据3-1', '数据3-2', '数据3-3']
                ],
                'stripe': True,
                'border': True
            },
            'timeline': {
                'items': [
                    {
                        'time': '2023年12月',
                        'title': '事件一',
                        'content': '这是事件一的详细描述'
                    },
                    {
                        'time': '2023年8月',
                        'title': '事件二',
                        'content': '这是事件二的详细描述'
                    },
                    {
                        'time': '2023年3月',
                        'title': '事件三',
                        'content': '这是事件三的详细描述'
                    }
                ],
                'direction': 'vertical'
            },
            'divider': {
                'style': 'solid',
                'color': '#DDDDDD',
                'margin': '20px 0'
            },
            'custom_html': {
                'content': '<div class="custom-container"><h3>自定义HTML示例</h3><p>这是一个使用自定义HTML的示例内容。</p></div>',
                'styles': '.custom-container { padding: 15px; border: 1px solid #eee; border-radius: 4px; }'
            }
        }

        for component_type, data in demo_data.items():
            component = Component.objects.filter(type=component_type).first()
            if component:
                component.demo_data = data
                component.save()
                self.stdout.write(f'创建演示数据: {component.name}') 