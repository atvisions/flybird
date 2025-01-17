from django.apps import AppConfig


class ResumeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resume'
    verbose_name = '简历管理'

    def ready(self):
        try:
            import resume.signals  # noqa
        except ImportError:
            pass 