# ************************************************************
# * Events API.
# * Created by Kryukov A.(ekryukov@icloud.com)  at 10.05.2016
# *************************************************************

import logging

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sequences import get_next_value

from core.com.api import get_dict_choice
from core.com.models import BaseLang, Dictionary
from core.ost.models import DEFAULT_INST
from core.prc.models import get_session_id
from core.rul.models import load_params, execute_rule_set
from share.common import get_hash
from share.models import Base

logger = logging.getLogger(__name__)

event_shared_data = {}
event_object_tab = []
event_rule_tab = []
event_params = {}

EVENT_STATUS_KEY = 'EVST'
EVENT_STATUS_READY = 'EVST0001'
EVENT_STATUS_PROCESSED = 'EVST0002'
EVENT_STATUS_DO_NOT_PROCES = 'EVST0003'


class Event(BaseLang):
    """Events raising in the system for exact institution."""
    event_type = models.CharField(_("Event type"), max_length=8, help_text=_("Event type code."), unique=True)
    is_cached = models.BooleanField(_("Is cached"), default=False, help_text=_("Cached (delayed) rule set execution."))
    status_lov = models.ForeignKey('com.Lov', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "evt_event"
        verbose_name = _("Event")

    def save(self, *args, **kwargs):
        dict_code = 'EVNT'
        self.event_type = self.event_type.upper()
        code = self.event_type[4:].upper()
        d, created = Dictionary.objects.get_or_create(dict_code=dict_code, code=code)
        if created:
            d.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.event_type


class EventObject(Base):
    """Objects awaiting processing by subscribers."""
    event = models.ForeignKey('Event', on_delete=models.CASCADE, help_text=_("Reference to event."))
    procedure_name = models.CharField(_("Procedure name"), max_length=200, help_text=_("Subscriber procedure name."))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text=_("Business-entity type."))
    object_id = models.PositiveIntegerField(_("Reference to the object."))
    content_object = GenericForeignKey('content_type', 'object_id')
    eff_date = models.DateTimeField(_("Effective date"), help_text=_("Event effective date"))
    session = models.ForeignKey('prc.Session', related_name=_("Session"), help_text=_("Session identifier."),
                                on_delete=models.CASCADE)
    split_hash = models.PositiveIntegerField(_("Split hash"), default=-1,
                                             help_text=_("Hash value to split further processing."))
    status = models.CharField(_("Status"), help_text=_("Event status"), max_length=8, choices=get_dict_choice('EVST'))

    class Meta:
        db_table = "evt_event_object"
        verbose_name = _("Event object")


class EventType(Base):
    """Event types"""
    event_type = models.CharField(_("Event type"), max_length=8, help_text=_("Event type code."),
                                  choices=get_dict_choice('EVNT'))
    entity_type = models.CharField(_("Entity type"), max_length=8, help_text=_("Entity type code."),
                                   choices=get_dict_choice("ENTT"))

    class Meta:
        db_table = "evt_event_type"
        verbose_name = _("Event type")

    def __str__(self):
        return "{}::{}".format(self.event_type, self.entity_type)

    @property
    def event_type_raw(self):
        return self.event_type

    @property
    def entity_type_raw(self):
        return self.entity_type


class Subscriber(models.Model):
    """Processes subscribed on events to process objects linked with event."""
    procedure_name = models.CharField(_("Procedure name"), max_length=200, help_text=_("Subscriber procedure name."))
    event_type = models.CharField(_("Event type"), max_length=8, help_text=_("Reference to event."))
    priority = models.PositiveSmallIntegerField(_("Priority"), default=10, help_text=_(
        "Event processing priority when subscriber process few events."))
    event = models.ManyToManyField(Event, through='Subscription')

    def __str__(self):
        return "{}::{}".format(self.event_type, self.procedure_name)

    class Meta:
        db_table = "evt_subscriber"
        verbose_name = _("Subscriber")


class Subscription(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    modifier = models.ForeignKey("rul.Modifier", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'evt_subscription'
        verbose_name = _("Subscription")


class EventRuleSet(models.Model):
    """Rule sets executing when events raised"""
    event = models.ForeignKey('Event', on_delete=models.CASCADE, help_text=_("Reference to event."))
    rule_set = models.ForeignKey('rul.RuleSet', on_delete=models.CASCADE, help_text=_("Reference to rule set."))
    modifier = models.ForeignKey('rul.Modifier', on_delete=models.CASCADE, help_text=_(
        "Modifier containing filter on objects will processed by current rule set."), null=True)


def get_subscriber_tab(event_type):
    """Get list of subscribers for event type"""
    subscriber_tab = []
    a = Subscription.objects.filter(event__event_type=event_type)
    if a.count() > 0:
        subscriber_tab = [{"event_id": x.event_id, "mod_id": x.modifier.id, "proc_name": x.subscriber.procedure_name}
                          for x in a]
    return subscriber_tab


def get_rule_set_tab(event_type):
    """Get list"""
    rule_set_tab = []
    a = EventRuleSet.objects.filter(event__event_type=event_type)
    if a.count() > 0:
        rule_set_tab = [(x.modifier_id, x.rule_set_id, x.event.is_cached) for x in a]
    return rule_set_tab


def register_event(event_type, eff_date, entity_type, object_id, param_tab, status=None, inst_id=DEFAULT_INST):
    """Register event"""
    rec_tab = {}
    logger.debug(_("Incoming event {} {} {} {}".format(
        event_type,
        eff_date,
        ":".join((entity_type, str(object_id))),
        status
    )))

    split_hash = get_hash(object_id, settings.SPLIT_DEGREE)
    l_param_tab = param_tab
    l_param_tab["EVENT_TYPE"] = event_type
    l_param_tab["EVENT_DATE"] = eff_date
    l_param_tab["ENTITY_TYPE"] = entity_type
    l_param_tab["OBJECT_ID"] = object_id
    l_param_tab["INST_ID"] = inst_id
    l_param_tab["SPLIT_HASH"] = split_hash

    load_params(entity_type=entity_type, object_id=object_id, param_tab=l_param_tab)

    subscriber_tab = get_subscriber_tab(event_type)
    cnt = 0
    for rec in subscriber_tab:
        logger.debug("Asserting modifier {}".format(rec["mod_id"]))

        #  TODO check condition - check modifier parameters
        rec_tab.clear()
        rec_tab["event_object_id"] = get_next_value('event_object_id')
        rec_tab["event_id"] = rec["event_id"]
        rec_tab["procedure_name"] = rec["proc_name"]
        rec_tab["entity_tab"] = entity_type
        rec_tab["object_id"] = object_id
        rec_tab["eff_date"] = eff_date
        rec_tab["inst_id"] = inst_id
        rec_tab["split_hash"] = split_hash
        rec_tab["status"] = status or EVENT_STATUS_READY
        rec_tab["session_id"] = get_session_id

        event_object_tab.extend(rec_tab)

        cnt += 1

        if cnt > 1000:
            flush_events()
    flush_events()


def cancel_events():
    event_object_tab.clear()
    event_rule_tab.clear()


def flush_events():
    logger.debug("Going to flush {} subscriptions".format(len(event_object_tab)))
    content_object = None
    cnt = 0
    for rec in event_object_tab:
        e = EventObject()
        e.pk = rec["event_object_id"]
        e.event_id = rec["event_id"]
        e.procedure_name = rec["procedure_name"]
        e.eff_date = rec["eff_date"]

        e.content_object = content_object
        e.session_id = rec["session_id"]
        e.split_hash = rec["split_hash"]
        e.status = rec["status"]
        e.save()
        cnt += 1

    logger.debug(' {} Subscriptions saved'.format(cnt))

    event_object_tab.clear()

    for rec in event_rule_tab:
        event_params.clear()

        event_params['EVENT_TYPE'] = rec["event_type"]
        event_params['EVENT_DATE'] = rec["event_date"]
        event_params['ENTITY_TYPE'] = rec["entity_type"]
        event_params['OBJECT_ID'] = rec["object_id"]
        event_params['INST_ID'] = rec["inst_id"]
        event_params['SPLIT_HASH'] = rec["split_hash"]

        # get object parameters
        load_params(entity_type=rec["entity_type"], object_id=rec["object_id"], param_tab=event_params)

        cnt = execute_rule_set(rec.rule_set_id, event_params)
        logger.debug("Count of runs: %d" % cnt)

    event_rule_tab.clear()
