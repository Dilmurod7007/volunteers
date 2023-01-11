from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VolunteerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'volunteer'
    verbose_name = _('Volontyor')
    verbose_name_plural = _('Volontyorlar') # ozgarishi mumkin
