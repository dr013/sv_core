# system
import logging

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.db import models
# django
from django.utils.translation import ugettext as _

# app
from sv_core.core.com.api import get_lov_choice
from sv_core.core.com.models import BaseLang
from sv_core.core.ost.models import DEFAULT_INST

logger = logging.getLogger(__name__)


class ViewableManager(models.Manager):
    def get_query_set(self):
        default_queryset = super(ViewableManager, self).get_queryset()
        return default_queryset.filter(user__is_active=True)


class Empl(models.Model):
    """ Custom extend for django class  User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skype = models.CharField(max_length=32, verbose_name=_('Skype'), null=True, blank=True)
    lang = models.CharField(max_length=8, verbose_name=_('Language'), help_text=_('Interface language'),
                            choices=settings.LANG_CHOICE)
    parent_id = models.ForeignKey('self', null=True, blank=True, limit_choices_to={'user__is_active': True},
                                  on_delete=models.SET_NULL)
    inst = models.ForeignKey('ost.Institution', on_delete=models.SET_DEFAULT, default=DEFAULT_INST)

    class Meta:
        verbose_name_plural = _(u'Employee')
        db_table = u'acm_user'
        permissions = (
            ("staff", "Can edit in backend"),
            ("simple", "Can view product info"),
        )

    @property
    def email_name(self):
        """Returns the person's full name."""
        return '%s %s <%s>' % (self.user.first_name, self.user.last_name, self.user.email)

    admin_objects = models.Manager()
    objects = ViewableManager()

    def __str__(self):
        return self.user.username


SECTION_TYPE = [
    ('Page', 'page'),
    ('Folder', 'folder'),
    ('Modal', 'modal'),
]


class Section(BaseLang):
    """Module sections. Logical parts of user interface."""
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL,
                               help_text=_('Parent section identifier'))
    module_code = models.CharField(max_length=8, verbose_name=_('Module code'),
                                   help_text=_('Reference to system module. Module code.'), choices=get_lov_choice(65))
    action = models.CharField(max_length=200, help_text=_('Django navigation action'), null=True, blank=True)
    section_type = models.CharField(max_length=8, help_text=_('Section type (folder, page).'), null=True, blank=True,
                                    choices=SECTION_TYPE)
    is_visible = models.BooleanField(verbose_name=_('Is visible'), default=True,
                                     help_text=_('Flag to display section like menu element.'))
    display_order = models.PositiveSmallIntegerField(help_text=_('Item display order in menu list.'), null=True,
                                                     blank=True)
    permission = models.ManyToManyField(Permission)

    class Meta:
        verbose_name_plural = _(u'Section')
        ordering = ['display_order']

    def __str__(self):
        return '%s:%s' % (self.name, self.section_type)


class AgentEmpl(models.Model):
    agent = models.ForeignKey('ost.Agent', on_delete=models.CASCADE)
    empl = models.ForeignKey(Empl, limit_choices_to={'user__is_active': True}, on_delete=models.CASCADE)
    is_head = models.BooleanField(default=False)

    def __str__(self):
        return '%s :: %s' % (self.agent, self.empl.user.username)

    class Meta:
        unique_together = (('agent', 'empl'),)


def create_user(username, email=None, first_name=None, last_name=None, password=None):
    user = User(username=username, first_name=first_name, last_name=last_name, email=email)
    user.is_staff = False
    user.is_superuser = False
    user.set_password(password)
    user.save()
    permission = Permission.objects.get(codename='run_report')
    user.user_permissions.add(permission)
    permission = Permission.objects.get(codename='change_empl')
    user.user_permissions.add(permission)
    permission = Permission.objects.get(codename='simple')
    user.user_permissions.add(permission)
    user.save()
    empl = Empl(user=user)
    empl.save()

    # mail == Email Address
    if not email:
        email = '%s@%s' % (username, settings.DEFAULT_DOMEN)
        user.email = email
        user.save()
