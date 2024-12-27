from django.apps import AppConfig

class MembershipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'membership'
    verbose_name = '会员管理'

    def ready(self):
        import membership.signals 