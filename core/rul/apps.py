from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RulConfig(AppConfig):
    name = 'core.rul'
    verbose_name = _("Rule")
