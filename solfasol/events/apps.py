from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EventsConfig(AppConfig):
    name = 'solfasol.events'
    verbose_name = _('events')
