from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SecureConfig(AppConfig):
    name = "sec"
    verbose_name = _("Security")
