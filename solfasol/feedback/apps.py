from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FeedbackConfig(AppConfig):
    name = 'solfasol.feedback'
    verbose_name = _('feedback')
