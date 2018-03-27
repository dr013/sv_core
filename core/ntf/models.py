# Created by 'Evgeny Krukov' at 08.11.13 10:57<
import logging

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.com.models import BaseLang

logger = logging.getLogger(__name__)


class Notification(models.Model):
    """Notification class"""
    name = models.CharField(_('Notification name'), max_length=8)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Уведомления')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        u"""
        Code name to uppercase
        """
        if self.name:
            self.name = self.name.upper()
        super(Notification, self).save(*args, **kwargs)


class SubscribeGroup(models.Model):
    group = models.CharField(verbose_name=_('Group Name'), help_text=_('Group of subscribers'), max_length=200)
    is_active = models.BooleanField(verbose_name=_('Is active group'), default=True)
    notification = models.ManyToManyField(Notification, db_table='ntf_group_notification')

    def __str__(self):
        return self.group


class Subscriber(models.Model):
    group = models.ForeignKey(SubscribeGroup, on_delete=models.SET_NULL, null=True)
    empl = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def email(self):
        return self.empl.email

    def __str__(self):
        return 'Group %s - %s %s<%s>' % (self.group, self.empl.first_name, self.empl.last_name, self.empl.email)

    class Meta:
        db_table = 'ntf_subscriber'
        verbose_name = _("Subscriber")


class Channel(models.Model):
    """Possible channels of message delivery."""
    address_pattern = models.CharField(_("Address pattern"), max_length=200)
    mess_max_length = models.PositiveIntegerField(_("Message length"), help_text=_("Maximum length of message text."))
    address_source = models.CharField(_("Address source"), max_length=2000, help_text=_(
        "Procedure name returning address string. Address extracting from notified entity."))

    class Meta:
        db_table = "ntf_channel"
        verbose_name = _("Channel")


class Message(models.Model):
    """Messages prepared for delivery."""
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True)
    text = models.TextField(_("Text"), help_text=_("Message content."))
    lang = models.CharField(_("Language"), max_length=8, help_text=_("Message language."))
    delivery_address = models.CharField(_("Address"), max_length=200, help_text=_("Delivery address."))
    delivery_date = models.DateTimeField(_("Delivery date"),
                                         help_text=_("Delivery date. Message can be delivered after that date."))
    is_delivered = models.BooleanField(_("Is delivered"), default=False, help_text=_("Flag if message was delivered."))
    urgency_level = models.PositiveSmallIntegerField(_("Urgency level"), default=1, help_text=_(
        "Message urgency level (0 - high urgency, 1- normal urgency, 2 - low urgency etc)"))
    event_type = models.CharField(_("Event type"), max_length=8, help_text=_("Event type code."))
    eff_date = models.DateField(_("Effective date"), null=True, blank=True, help_text=_("Event effective date."))
    gate_ref = models.PositiveIntegerField(_("Gateway reference"), null=True, blank=True,
                                           help_text=_("Message identifier for updating status from gateway."))
    message_status = models.CharField(_("Message status"), max_length=8,
                                      help_text=_("Status of message from gateway (dictionary SGMS)."))

    class Meta:
        db_table = "ntf_message"
        verbose_name = _("Message")


class Template(models.Model):
    """Notification templates"""
    notification = models.ForeignKey(Notification, on_delete=models.SET_NULL, related_name=_("Notification"),
                                     help_text=_("Reference to notification."), null=True)
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, related_name=_("Channel"),
                                help_text=_("Reference to delivery channel."), null=True)
    lang = models.CharField(_("Language"), max_length=8, help_text=_("Multi language template support."))
    report_template = models.ForeignKey("rpt.Template", on_delete=models.SET_NULL,
                                        help_text=_("Message template for reports generation system."), null=True)

    class Meta:
        db_table = "ntf_template"
        verbose_name = _("Notification template")


class Scheme(BaseLang):
    """Notification schemes."""
    scheme_type = models.CharField(_("Scheme type"), max_length=8, help_text=_("Notification scheme type."))

    # inst_id

    class Meta:
        db_table = "ntf_scheme"
        verbose_name = _("Scheme")
