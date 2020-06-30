from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class IssuesConfig(AppConfig):
    name = 'solfasol.issues'
    verbose_name = _('issues')
