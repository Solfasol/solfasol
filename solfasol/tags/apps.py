from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TagsConfig(AppConfig):
    name = 'solfasol.tags'
    verbose_name = _('tags')
