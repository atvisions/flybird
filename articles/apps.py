from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'
    verbose_name = _('文章管理') 