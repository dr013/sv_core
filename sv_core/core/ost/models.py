from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sv_core.core.com.models import BaseLang
from sv_core.core.com.models import Lov
from sv_core.core.com.models import Parameter

INSTANCE_TYPE = [
    (u'ISTPSSH', _("Server ssh access")),
    (u'ISTPSBVN', _("SVN repository")),
    ('ISTPGIT', _("Git repository")),
    (u'ISTPORCL', _("Oracle database")),
    (u'ISTPPSGR', _("PostgreSQL database")),
    (u'ISTPJIRA', _("JIRA is the project tracker")),
]

DEFAULT_INST = 9999


class Institution(BaseLang):
    identity = models.PositiveSmallIntegerField(primary_key=True, db_column='id', unique=True, db_index=True)
    seqnum = models.PositiveSmallIntegerField(default=1, editable=False)
    parent_id = models.ForeignKey('Institution', blank=True, null=True, related_name='child_set',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return u'%s-%s' % (self.identity, self.name)

    class Meta:
        permissions = (
            ("view_inst", "Can view institution"),
        )
        db_table = 'ost_institution'


class InstanceType(BaseLang):
    instance_type = models.CharField(max_length=8, verbose_name=_("Instance type"), choices=INSTANCE_TYPE)
    connect_tmpl = models.CharField(max_length=200, verbose_name=_("Connect template"), null=True, blank=True)

    class Meta:
        verbose_name = _("Instance type")
        verbose_name_plural = verbose_name
        db_table = 'ost_instance_type'

    def __str__(self):
        return '%s - %s' % (self.id, self.name)


class InstanceTypeParameter(models.Model):
    instance_type = models.ForeignKey(InstanceType, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(db_column="ord", verbose_name=_("Ordering"))
    lov = models.ForeignKey(Lov, blank=True, null=True, on_delete=models.SET_NULL)
    default_value = models.CharField(verbose_name=_("Default value"), max_length=2000, null=True, blank=True)
    is_required = models.BooleanField(verbose_name=_("Required"), default=True)

    class Meta:
        db_table = "ost_inst_type_parameter"
        verbose_name = _("Instance type parameter")
        verbose_name_plural = _("Instance type parameters")
        ordering = ['order',]

    def __str__(self):
        return '%s %s' % (self.instance_type.instance_type, self.parameter)


class Server(models.Model):
    """
    Servers
    """
    address_ip = models.GenericIPAddressField(verbose_name=_('IP'))
    address_name = models.CharField(max_length=200, verbose_name=_('Host name'))
    is_local = models.BooleanField(default=True, verbose_name=_('Is local server'))
    root_access = models.BooleanField(default=True, verbose_name=_('Have a root access'))
    server_name = models.CharField(max_length=32, verbose_name=_('Server name'))
    desc = models.CharField(max_length=200, verbose_name=_('Server description'), null=True, blank=True)
    inst = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s(%s)-%s' % (self.server_name, self.address_ip, self.desc)

    class Meta:
        unique_together = ("address_ip", "server_name")
        db_table = "ost_server"


class Instance(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    instance_type = models.ForeignKey(InstanceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name=_("Instance name"))

    def __str__(self):
        return u'%s - %s' % (self.server.server_name, self.name)

    class Meta:
        unique_together = ("name",)
        permissions = (
            ("view", "Can view instance"),
        )
        db_table = "ost_instance"


class InstanceParameterValue(models.Model):
    instance_parameter = models.ForeignKey(InstanceTypeParameter, on_delete=models.CASCADE)
    parameter_value = models.CharField(max_length=200, db_column="param_value")
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)

    class Meta:
        db_table = "ost_instance_parameter_value"
        verbose_name = _("Parameter value")

    def __str__(self):
        return u'%s %s := %s' % (self.instance, self.instance_parameter.parameter.name, self.parameter_value)


class Agent(models.Model):
    inst = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name=_("Internal group"))
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ost_agent"
        verbose_name = _("Internal group")
