from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AcmConfig(AppConfig):
    name = 'sv_core.core.acm'
    verbose_name = _("Access management")
