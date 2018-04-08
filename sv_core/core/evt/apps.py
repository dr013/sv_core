from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EventConfig(AppConfig):
    name = "evt"
    verbose_name = _("Event")
