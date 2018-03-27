from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NtfConfig(AppConfig):
    name = 'core.ntf'
    verbose_name = _("Notification")
