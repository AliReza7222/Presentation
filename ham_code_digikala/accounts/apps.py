from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ham_code_digikala.accounts'

    def ready(self):
        import ham_code_digikala.accounts.signals
