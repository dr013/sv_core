from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OrganizationalStructureConfig(AppConfig):
    name = "core.ost"
    verbose_name = _("Organizational Structure")
