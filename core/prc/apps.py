from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PrcConfig(AppConfig):
    name = 'core.prc'
    verbose_name = _("Process")