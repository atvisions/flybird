from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = '用户管理'

    def ready(self):
        import users.signals  # 导入信号模块 