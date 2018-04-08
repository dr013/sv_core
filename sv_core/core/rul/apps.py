from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RuleConfig(AppConfig):
    name = "rul"
    verbose_name = _("Rule")
