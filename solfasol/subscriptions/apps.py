from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SubscriptionsConfig(AppConfig):
    name = 'solfasol.subscriptions'
    verbose_name = _('subscriptions')
