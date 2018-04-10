from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EventConfig(AppConfig):
    name = "sv_core.core.evt"
    verbose_name = _("Event")
