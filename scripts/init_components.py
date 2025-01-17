import os
import sys
import django

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from resume.models import ComponentCategory, Component

def init_components():
    # 创建布局分类
    layout_category, _ = ComponentCategory.objects.get_or_create(
        code='layout',
        defaults={
            'name': '布局',
            'icon': 'mdi-view-dashboard',
            'description': '简历布局',
            'sort_order': 1,
            'is_active': True
        }
    )

    # 创建组件分类
    component_category, _ = ComponentCategory.objects.get_or_create(
        code='component',
        defaults={
            'name': '组件',
            'icon': 'mdi-puzzle',
            'description': '简历组件',
            'sort_order': 2,
            'is_active': True
        }
    )

    # 创建布局组件
    layout_components = [
        {
            'name': '单栏布局',
            'type': 'layout',
            'icon': 'mdi-view-sequential',
            'description': '适用于简洁的个人简历',
            'category': layout_category,
            'config': {
                'type': 'single',
                'columns': 1
            }
        },
        {
            'name': '双栏布局',
            'type': 'layout',
            'icon': 'mdi-view-parallel',
            'description': '适用于信息较多的简历',
            'category': layout_category,
            'config': {
                'type': 'double',
                'columns': 2
            }
        },
        {
            'name': '三栏布局',
            'type': 'layout',
            'icon': 'mdi-view-column',
            'description': '适用于内容丰富的简历',
            'category': layout_category,
            'config': {
                'type': 'triple',
                'columns': 3
            }
        }
    ]

    # 创建基本组件
    basic_components = [
        {
            'name': '基本信息',
            'type': 'contact',
            'icon': 'mdi-account',
            'description': '姓名、职位、联系方式等基本信息',
            'category': component_category,
            'config': {
                'fields': [
                    {
                        'name': 'username',
                        'label': '用户名',
                        'type': 'text',
                        'required': True,
                        'placeholder': '请输入用户名'
                    },
                    {
                        'name': 'phone',
                        'label': '手机号码',
                        'type': 'tel',
                        'required': True,
                        'placeholder': '请输入手机号码'
                    },
                    {
                        'name': 'email',
                        'label': '邮箱',
                        'type': 'email',
                        'required': False,
                        'placeholder': '请输入邮箱'
                    },
                    {
                        'name': 'position',
                        'label': '职位',
                        'type': 'text',
                        'required': False,
                        'placeholder': '请输入职位'
                    },
                    {
                        'name': 'bio',
                        'label': '个人简介',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': '请输入个人简介'
                    }
                ],
                'style': {
                    'padding': '16px',
                    'background': '#ffffff',
                    'border': '1px solid #e4e7ed',
                    'borderRadius': '4px'
                }
            }
        }
    ]

    # 批量创建布局组件
    for component_data in layout_components:
        Component.objects.get_or_create(
            name=component_data['name'],
            defaults={
                'type': component_data['type'],
                'icon': component_data['icon'],
                'description': component_data['description'],
                'category': component_data['category'],
                'config': component_data['config'],
                'is_system': True
            }
        )

    # 批量创建基本组件
    for component_data in basic_components:
        Component.objects.get_or_create(
            name=component_data['name'],
            defaults={
                'type': component_data['type'],
                'icon': component_data['icon'],
                'description': component_data['description'],
                'category': component_data['category'],
                'config': component_data['config'],
                'is_system': True
            }
        )

    print('组件初始化完成!')

if __name__ == '__main__':
    init_components() 