# Copyright (C) 2018 Eugene Kryukov<ekryukov@icloud.com>
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CommonConfig(AppConfig):
    name = "com"
    verbose_name = _("Common")
