from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SecureConfig(AppConfig):
    name = "core.sec"
    verbose_name = _("Security")
