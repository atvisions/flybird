import os
import sys
import django

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from resume.models import ComponentCategory, Component

def init_layout_components():
    # 创建布局分类
    layout_category, _ = ComponentCategory.objects.get_or_create(
        name='布局',
        defaults={
            'icon': 'mdi-view-dashboard',
            'description': '简历布局',
            'sort_order': 1,
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
                'layout': {
                    'type': 'single',
                    'columns': 1,
                    'gap': '1rem',
                    'backgroundColor': '#000000'
                }
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
                'columns': 2,
                'style': {
                    'container': {
                        'padding': '20px',
                        'gap': '20px'
                    },
                    'column': {
                        'padding': '16px',
                        'backgroundColor': '#f5f7fa',
                        'border': '2px dashed #e4e7ed',
                        'borderRadius': '8px',
                        'gap': '12px'
                    },
                    'placeholder': {
                        'minHeight': '120px',
                        'backgroundColor': '#ffffff',
                        'borderRadius': '6px'
                    },
                    'item': {
                        'padding': '16px',
                        'backgroundColor': '#ffffff',
                        'border': '1px solid #e4e7ed',
                        'borderRadius': '6px',
                        'boxShadow': '0 2px 6px rgba(0, 0, 0, 0.04)'
                    }
                }
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
                'columns': 3,
                'style': {
                    'container': {
                        'padding': '20px',
                        'gap': '20px'
                    },
                    'column': {
                        'padding': '16px',
                        'backgroundColor': '#f5f7fa',
                        'border': '2px dashed #e4e7ed',
                        'borderRadius': '8px',
                        'gap': '12px'
                    },
                    'placeholder': {
                        'minHeight': '120px',
                        'backgroundColor': '#ffffff',
                        'borderRadius': '6px'
                    },
                    'item': {
                        'padding': '16px',
                        'backgroundColor': '#ffffff',
                        'border': '1px solid #e4e7ed',
                        'borderRadius': '6px',
                        'boxShadow': '0 2px 6px rgba(0, 0, 0, 0.04)'
                    }
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

    print('布局组件初始化完成!')

if __name__ == '__main__':
    init_layout_components() 