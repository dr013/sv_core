from django.db import models
from django.utils.translation import ugettext_lazy as _

from sv_core.share.models import Base


class Session(Base):
    class Meta:
        db_table = 'prc_session'
        verbose_name = _("Session")
        ordering = ['-created_at']

    is_finish = models.BooleanField(_("Is finished"), default=False)

    def __str__(self):
        return "Session #%s" % str(self.pk).zfill(8)


def get_session_id():
    a = Session.objects.filter(is_finish=False)
    if a:
        result = a.id
    else:
        result = None

    return result
