from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = _('Yangiliklar')
    verbose_name_plural = _('Yangiliklar') # ozgarishi mumkin
