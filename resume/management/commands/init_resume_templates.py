from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resume.models import ResumeTemplate, TemplateCategory, ComponentCategory

User = get_user_model()

class Command(BaseCommand):
    help = '初始化简历模板数据'

    def handle(self, *args, **kwargs):
        # 确保有管理员用户
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@example.com'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # 创建模板分类
        category, _ = TemplateCategory.objects.get_or_create(
            name='基础模板',
            defaults={
                'icon': 'mdi-file-document-outline',
                'description': '基础简历模板',
                'sort_order': 0,
            }
        )

        # 创建单栏布局模板
        single_template = {
            'name': '简约单栏简历模板',
            'description': '一个简洁的单栏布局简历模板，适合传统风格的简历',
            'creator': admin_user,
            'category': category,
            'status': 'approved',
            'is_vip': False,
            'price': 0,
            'components': [
                {
                    'id': 1,
                    'type': 'basic-info',
                    'config': {
                        'fields': {
                            'name': '',
                            'title': '',
                            'email': '',
                            'phone': '',
                            'summary': ''
                        },
                        'styles': {
                            'padding': '20px',
                            'background': '#ffffff',
                            'borderRadius': '8px',
                            'marginBottom': '16px'
                        },
                        'layout': {
                            'x': 0,
                            'y': 0,
                            'w': 12,
                            'h': 3
                        }
                    }
                },
                {
                    'id': 2,
                    'type': 'education',
                    'config': {
                        'fields': {
                            'items': []
                        },
                        'styles': {
                            'padding': '20px',
                            'background': '#ffffff',
                            'borderRadius': '8px',
                            'marginBottom': '16px'
                        },
                        'layout': {
                            'x': 0,
                            'y': 3,
                            'w': 12,
                            'h': 4
                        }
                    }
                },
                {
                    'id': 3,
                    'type': 'experience',
                    'config': {
                        'fields': {
                            'items': []
                        },
                        'styles': {
                            'padding': '20px',
                            'background': '#ffffff',
                            'borderRadius': '8px',
                            'marginBottom': '16px'
                        },
                        'layout': {
                            'x': 0,
                            'y': 7,
                            'w': 12,
                            'h': 6
                        }
                    }
                }
            ],
            'layout': {
                'type': 'grid',
                'columns': 12,
                'gap': '16px',
                'areas': [
                    {
                        'name': 'header',
                        'x': 0,
                        'y': 0,
                        'w': 12,
                        'h': 3
                    },
                    {
                        'name': 'main',
                        'x': 0,
                        'y': 3,
                        'w': 12,
                        'h': 10
                    }
                ]
            },
            'theme': {
                'colors': {
                    'primary': '#2c3e50',
                    'secondary': '#7f8c8d',
                    'background': '#f5f7fa',
                    'accent': '#3498db'
                },
                'typography': {
                    'title': {
                        'font': 'Arial',
                        'size': '24px',
                        'weight': 'bold'
                    },
                    'body': {
                        'font': 'Arial',
                        'size': '14px',
                        'weight': 'normal'
                    }
                },
                'spacing': {
                    'unit': '1rem',
                    'section': '2rem'
                }
            }
        }

        # 创建双栏布局模板
        double_template = {
            'name': '现代双栏简历模板',
            'description': '一个现代风格的双栏布局简历模板，左侧放置基本信息和技能，右侧放置经历',
            'creator': admin_user,
            'category': category,
            'status': 'approved',
            'is_vip': False,
            'price': 0,
            'components': [
                {
                    'id': 1,
                    'type': 'basic-info',
                    'config': {
                        'fields': {
                            'name': '',
                            'title': '',
                            'email': '',
                            'phone': '',
                            'summary': ''
                        },
                        'styles': {
                            'padding': '20px',
                            'background': '#ffffff',
                            'borderRadius': '8px',
                            'marginBottom': '16px'
                        },
                        'layout': {
                            'x': 0,
                            'y': 0,
                            'w': 4,
                            'h': 3
                        }
                    }
                },
                {
                    'id': 2,
                    'type': 'skills',
                    'config': {
                        'fields': {
                            'categories': []
                        },
                        'styles': {
                            'padding': '20px',
                            'background': '#ffffff',
                            'borderRadius': '8px',
                            'marginBottom': '16px'
                        },
                        'layout': {
                            'x': 0,
                            'y': 3,
                            'w': 4,
                            'h': 4
                        }
                    }
                },
                {
                    'id': 3,
                    'type': 'education',
                    'config': {
                        'fields': {
                            'items': []
                        },
                        'styles': {
                            'padding': '20px',
                            'background': '#ffffff',
                            'borderRadius': '8px',
                            'marginBottom': '16px'
                        },
                        'layout': {
                            'x': 4,
                            'y': 0,
                            'w': 8,
                            'h': 4
                        }
                    }
                },
                {
                    'id': 4,
                    'type': 'experience',
                    'config': {
                        'fields': {
                            'items': []
                        },
                        'styles': {
                            'padding': '20px',
                            'background': '#ffffff',
                            'borderRadius': '8px',
                            'marginBottom': '16px'
                        },
                        'layout': {
                            'x': 4,
                            'y': 4,
                            'w': 8,
                            'h': 6
                        }
                    }
                }
            ],
            'layout': {
                'type': 'grid',
                'columns': 12,
                'gap': '16px',
                'areas': [
                    {
                        'name': 'sidebar',
                        'x': 0,
                        'y': 0,
                        'w': 4,
                        'h': 12
                    },
                    {
                        'name': 'main',
                        'x': 4,
                        'y': 0,
                        'w': 8,
                        'h': 12
                    }
                ]
            },
            'theme': {
                'colors': {
                    'primary': '#34495e',
                    'secondary': '#95a5a6',
                    'background': '#ecf0f1',
                    'accent': '#e74c3c'
                },
                'typography': {
                    'title': {
                        'font': 'Arial',
                        'size': '24px',
                        'weight': 'bold'
                    },
                    'body': {
                        'font': 'Arial',
                        'size': '14px',
                        'weight': 'normal'
                    }
                },
                'spacing': {
                    'unit': '1rem',
                    'section': '2rem'
                }
            }
        }

        # 保存模板
        for template_data in [single_template, double_template]:
            template, created = ResumeTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    'description': template_data['description'],
                    'creator': template_data['creator'],
                    'category': template_data['category'],
                    'status': template_data['status'],
                    'is_vip': template_data['is_vip'],
                    'price': template_data['price'],
                    'components': template_data['components'],
                    'layout': template_data['layout'],
                    'theme': template_data['theme']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created template "{template.name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Template "{template.name}" already exists')
                ) 