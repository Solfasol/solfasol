from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ContributorsConfig(AppConfig):
    name = 'solfasol.contributors'
    verbose_name = _('contributors')
