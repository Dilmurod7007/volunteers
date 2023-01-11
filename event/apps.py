from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EventConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event'
    verbose_name = _('Tadbir')
    verbose_name_plural = _('Tadbirlar') # ozgarishi mumkin
