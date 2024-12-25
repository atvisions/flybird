from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class QaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qa'
    verbose_name = _('问答管理') 