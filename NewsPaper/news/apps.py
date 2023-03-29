"""конфигурирования приложения"""
from django.apps import AppConfig


class NewsConfig(AppConfig):
    """класс Config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = "Новости и статьи"

    def ready(self):
        import news.signals
