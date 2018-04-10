import importlib
import logging

from django.db import models, connection
from django.utils.translation import ugettext_lazy as _

from sv_core.core.com.api import get_dict_choice
from sv_core.core.com.models import BaseLang
from sv_core.share.common import lookahead

rul_shared_data = {}
logger = logging.getLogger(__name__)


class NameFormat(BaseLang):
    """Format description for generation of name"""
    # inst = models.ForeignKey(Institution, help_text=_('Owner institution identifier'), default=9999)
    seqnum = models.PositiveSmallIntegerField(help_text=_('Sequential number of data version'), default=1,
                                              editable=False)
    entity_type = models.CharField(max_length=8, help_text=_('Entity type'))  # choices=get_lov_choice(7)
    name_length = models.PositiveSmallIntegerField(help_text=_('Length of name'), blank=True, null=True)
    pad_type = models.CharField(max_length=8, help_text=_('Padding method'))
    pad_string = models.CharField(max_length=200, help_text=_('Padding string'))
    check_algorithm = models.CharField(max_length=8, help_text=_('Algorithm for check digit generation'))
    check_base_position = models.PositiveSmallIntegerField(
        help_text=_('Starting position of base for check digit calculation'), null=True, blank=True)
    check_base_length = models.PositiveSmallIntegerField(
        help_text=_('Ending position of base for check digit calculation'), null=True, blank=True)
    check_position = models.PositiveSmallIntegerField(help_text=_('Position for check digit'), null=True, blank=True)
    check_name = models.BooleanField(default=False, help_text=_('Checking name'))

    class Meta:
        verbose_name = _('Naming rule')
        db_table = 'rul_name_format'

    def __unicode__(self):
        return '%s-%s' % (self.pk, self.name)


class Modifier(BaseLang):
    """Scale modifiers """
    scale = models.ForeignKey('Scale', on_delete=models.CASCADE, help_text=_("Scale identifier"))
    condition = models.CharField(_("Condition"), max_length=2000, null=True, blank=True,
                                 help_text=_("Modifier condition"))
    priority = models.PositiveSmallIntegerField(_("Modifier priority"), default=10, help_text=_("Modifier priority"))

    class Meta:
        verbose_name = _("Modifier")
        db_table = 'rul_mod'


class Scale(BaseLang):
    """Scales by which attributes can be parametrised"""
    # inst = models.ForeignKey(Institution, help_text=_('Owner institution identifier'), default=9999)
    scale_type = models.CharField(_("Scale type"), max_length=8, choices=get_dict_choice("SCTP"),
                                  help_text=_("Category of scale"))

    class Meta:
        verbose_name = _("Modifier scale")
        db_table = "rul_mod_scale"


class RuleSet(BaseLang):
    """Sets of rules"""
    category = models.CharField(_("Category"), max_length=8, choices=get_dict_choice("RLCG"),
                                help_text=_("Category of rules set (RLCG key)"))

    class Meta:
        verbose_name = _("Rule set")
        db_table = "rul_rule_set"

    def __str__(self):
        return "{}::{}".format(self.pk, self.name)


class Rule(models.Model):
    """Assigment of procedures as processing rules"""
    rule_set = models.ForeignKey("RuleSet", on_delete=models.CASCADE, help_text=_("Rules set identifier"))
    procedure = models.ForeignKey("Procedure", on_delete=models.CASCADE, help_text=_("Procedure identifier"),
                                  db_column='proc_id')
    exec_order = models.PositiveSmallIntegerField(_("Execute order"), null=True,
                                                  help_text=_("Rule execution order within rules set"))

    class Meta:
        verbose_name = _("Rule")
        db_table = "rul_rule"
        ordering = ("id", "exec_order",)

    def __str__(self):
        return "{}::{}=>{}".format(self.pk, self.rule_set.name, self.procedure.proc_name)


class Procedure(BaseLang):
    """List of procedures used in rules"""
    proc_name = models.CharField(_("Procedure name"), max_length=200, help_text=_("Procedure name"))
    category = models.CharField(_("Category"), max_length=8, help_text=_("Category of procedure usage"),
                                choices=get_dict_choice("RLCG"))

    class Meta:
        verbose_name = _("Rule procedure")
        db_table = "rul_proc"

    def __str__(self):
        return "{}::{}".format(self.pk, self.proc_name)


class ProcedureParameter(BaseLang):
    """List of parameters of rules processing procedures"""
    proc = models.ForeignKey('Procedure', on_delete=models.CASCADE)
    param_name = models.CharField(_("Parameter name"), max_length=30)
    lov = models.ForeignKey('com.Lov', on_delete=models.SET_NULL, null=True, blank=True)
    display_order = models.PositiveSmallIntegerField(_("Display order"), default=10)
    is_mandatory = models.BooleanField(_("Is mandatory"), default=False)
    mod_param = models.ForeignKey('ModifierParameter', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'rul_proc_param'
        verbose_name = _("Procedure Parameter")
        ordering = ["display_order", ]

    def __str__(self):
        return '{}::{}'


class ParameterValue(models.Model):
    """Values of processing procedures parameters"""
    rule = models.ForeignKey("RuleSet", on_delete=models.CASCADE,
                             help_text=_("Action identifier (instance of procedure in rules set)"))
    param = models.ForeignKey("ProcedureParameter", on_delete=models.CASCADE, db_column='proc_param_id')
    value = models.CharField(_("Parameter value"), max_length=200, help_text=_("Parameter value"),
                             db_column='param_value')

    class Meta:
        db_table = 'rul_rule_param_value'
        verbose_name = _("Parameter Value")


class ModifierParameter(BaseLang):
    """Parameters which can be used in scales to parametrise attributes"""
    name = models.CharField(_("Parameter name"), max_length=200)
    data_type = models.CharField(_("Data type"), max_length=8, choices=get_dict_choice("DTTP"),
                                 help_text=_("Parameter data type"))
    lov = models.ForeignKey("com.Lov", on_delete=models.SET_NULL, null=True, blank=True,
                            help_text=_("List of Values identifier"))

    class Meta:
        db_table = 'rul_mod_param'
        verbose_name = _("Modifier Parameter")


def load_params(entity_type, object_id, param_tab):
    """Rule shared data by entity"""

    income_file_id = None

    # TODO Replace entity_type to django content type
    object_type = entity_type[4:]

    if object_type == 'RRFL':
        income_file_id = object_id


def set_param(name, value, param_tab):
    param_tab[name.upper()] = value
    logger.debug('Parameter {} value set to {}'.format(name, value))


def execute_rule_set(rule_set_id, event_params):
    cnt = 0
    io_params = {}
    sql = """
    SELECT
  rp.proc_name,
  rp.rule_id,
  rp.proc_id,
  rp.param_name,
  v.param_value,
  rp.is_mandatory,
  rp.param_id
FROM
  (SELECT
     p.proc_name,
     r.id  rule_id,
     p.id  proc_id,
     pp.id param_id,
     pp.param_name,
     r.exec_order,
     pp.is_mandatory
   FROM rul_rule r
     INNER JOIN rul_proc p ON p.id = r.proc_id
     LEFT OUTER JOIN rul_proc_param pp ON r.proc_id = pp.proc_id
   WHERE r.rule_set_id = %d) rp
  LEFT OUTER JOIN rul_rule_param_value v ON rp.rule_id = v.rule_id AND rp.param_id = v.proc_param_id
ORDER BY rp.exec_order
  , rp.rule_id
    """
    l_rule_tab = []

    with connection.cursor() as cursor:
        cursor.execute(sql % rule_set_id)
        for proc_name, rule_id, proc_id, param_name, param_value, is_mandatory, param_id in cursor.fetchall():
            d = dict(proc_name=proc_name, proc_id=proc_id, param_name=param_name, param_value=param_value,
                     is_mandatory=is_mandatory, param_id=param_id)
            l_rule_tab.append(d)

    for rec, has_more in lookahead(l_rule_tab):
        if rec['param_name'] is not None:
            if rec["is_mandatory"] and rec["param_value"] is None:
                logger.error("MANDATORY_PARAM_VALUE_NOT_DEFINED", rule_set_id=rule_set_id, rule_id=rec["rule_id"],
                             param_id=rec["param_id"], param_name=rec["param_name"])
                return

            io_params[rec["param_name"]] = rec["param_value"]
            if not has_more:
                cnt += 1
                logger.info('Executing rule [{rule_id}][{proc_name}] STARTING'.format(rule_id=rec["rule_id"],
                                                                                      proc_name=rec["proc_name"]))
                try:
                    module_name = ".execute.{}".format(rec["proc_name"])
                    run_module = importlib.import_module(module_name)
                    run_module.run(io_params)
                    logger.info("Executing rule [{rule_id}][{proc_name}'] FINISHED".format(rule_id=rec["rule_id"],
                                                                                           proc_name=rec["proc_name"]))

                except ImportError as err:
                    logger.fatal("Error import rule procedure {}".format(rec["proc_name"]))
                    logger.error(str(err))

            return cnt
