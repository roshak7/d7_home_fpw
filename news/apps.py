from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = 'Новости'

    def ready(self):
        # Для того, чтобы работали сигналы
        import news.signals
