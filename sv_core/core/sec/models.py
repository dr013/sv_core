from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

KEY_TYPE = (
    ("SKTP0001", _("Storage key")),
    ("SKTP0002", _("Transfer key")),
)
DEF_KEY_TYPE = "SKTP0001"


def get_year():
    return date(date.today().year, 12, 31)


class KeyManage(models.Model):
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    valid_till = models.DateField(_("Valid till"), default=get_year())
    key = models.CharField(_("Key"), max_length=4000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("User"))
    key_type = models.CharField(_("Secure key type"), max_length=8, default=DEF_KEY_TYPE, choices=KEY_TYPE)

    def __str__(self):
        return '%s - %s' % (self.user.get_full_name(), self.key[:40])

    class Meta:
        verbose_name = _('Encryption key')
        verbose_name_plural = _('Ключи шифрования PGP')
        db_table = 'sec_keymanage'
