import logging

from django.conf import settings
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from .api import get_dict_value

logger = logging.getLogger(__name__)

COLS = (
    ("NAME", _("Name")),
    ("DESCRIPTION", _("Description")),
)

DATA_TYPE = (
    ("DTTPCHAR", _("String")),
    ("DTTPNMBR", _("Number")),
    ("DTTPDATE", _("Date"))
)

LABEL_TYPE = (
    ("ERROR", _("Error")),
    ("FATAL", _("Fatal error")),
    ("INFO", _("Info")),
    ("LABEL", _("Label")),
    ("CAPTION", _("Caption")),
)


class I18n(models.Model):
    """Internalizations"""
    lang = models.CharField(max_length=8, help_text=_("Language code"), choices=settings.LANG_CHOICE,
                            verbose_name=_("Language"))
    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name=_("Entity_type"),
                                     on_delete=models.CASCADE, help_text=_("Type of entity - i18n value owner."))
    column_name = models.CharField(max_length=30, verbose_name=_("Column name"), choices=COLS,
                                   help_text=_("Virtual column name."))
    object_id = models.PositiveIntegerField(_("Object ID"), help_text=_("Reference to entity object."))
    text = models.TextField(_("Text"), help_text=_("Content of column in exact language."))
    entity = fields.GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = (('content_type', 'object_id', 'column_name', 'lang'),)
        db_table = 'com_i18n'


class BaseLang(models.Model):
    i18n = fields.GenericRelation(I18n)

    class Meta:
        abstract = True

    @property
    def name(self):
        cur_language = translation.get_language()
        logger.debug('Current lang is %s' % cur_language)
        rec_tab = self.i18n.all().filter(lang=settings.LANG[cur_language.lower()], column_name='NAME')
        if rec_tab:
            label = rec_tab[0].text
        else:
            rec_tab = self.i18n.all().filter(lang=settings.LANG[settings.LANGUAGE_CODE], column_name='NAME')
            if rec_tab:
                label = rec_tab[0].text
            else:
                label = ''

        return label

    @property
    def description(self):
        cur_language = translation.get_language()
        logger.debug('Current lang is %s' % cur_language)
        rec_tab = self.i18n.all().filter(lang=settings.LANG[cur_language.lower()], column_name='DESCRIPTION')
        if rec_tab:
            label = rec_tab[0].text
        else:
            rec_tab = self.i18n.all().filter(lang=settings.LANG[settings.LANGUAGE_CODE], column_name='DESCRIPTION')
            if rec_tab:
                label = rec_tab[0].text
            else:
                label = ''

        return label


class Lov(BaseLang):
    """List of values"""
    dictionary = models.CharField(max_length=8, db_column='dict', blank=True, null=True)
    lov_query = models.CharField(max_length=2000, null=True, blank=True, verbose_name=_('LoV query'),
                                 help_text=_('Query for list of values'))
    module_code = models.CharField(max_length=3, verbose_name='Code of module')
    sort_mode = models.CharField(max_length=8, blank=True, null=True)
    apperance = models.CharField(max_length=8, blank=True, null=True)
    data_type = models.CharField(max_length=8, verbose_name=_('Data type'), choices=DATA_TYPE)
    is_parametrized = models.BooleanField(default=False, verbose_name=_('Is parametrized'))

    class Meta:
        verbose_name = _('List of values')
        verbose_name_plural = verbose_name
        db_table = 'com_lov'

    def __str__(self):
        return '%s - %s' % (self.id, self.name)


class Dictionary(BaseLang):
    dict_code = models.CharField(max_length=4, db_column='dict', verbose_name=_('Dictionary article'),
                                 choices=get_dict_value())
    code = models.CharField(max_length=4, verbose_name=_('Code'))
    is_numeric = models.BooleanField(default=False, verbose_name=_('Is numeric'))
    is_editable = models.BooleanField(default=False, verbose_name=_('Is editable'))
    inst_id = models.PositiveSmallIntegerField(default=9999, verbose_name=_('Institution'))
    module_code = models.CharField(max_length=8, verbose_name=_('Module code'), default='COM')

    @property
    def dict_val(self):
        return '%s%s' % (self.dict_code, self.code)

    class Meta:
        verbose_name = _('Dictionary')
        db_table = 'com_dictionary'
        unique_together = (('dict_code', 'code'),)

    def __str__(self):
        if self.dict_code == 'DICT':
            return '%s: %s - %s(%s)' % (_('Dictionary'), self.code, self.name, self.description)
        else:
            return '%s %s(%s)' % (self.dict_val, self.name, self.description)

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        self.dict_code = self.dict_code.upper()
        self.module_code = self.module_code.upper()
        super().save(*args, **kwargs)


class Label(BaseLang):
    name = models.CharField(max_length=200, verbose_name=_('Label name'))
    label_type = models.CharField(max_length=8, verbose_name=_('Label type'), choices=LABEL_TYPE)
    module_code = models.CharField(max_length=3, verbose_name=_('Module code'))
    env_variable = models.CharField(max_length=200, verbose_name=_('Env variables'))

    class Meta:
        verbose_name = _('Label')
        db_table = 'com_label'

    def __str__(self):
        return '%s-%s', (self.name, self.label_type)


class Parameter(BaseLang):
    param_name = models.CharField(max_length=200, verbose_name=_('Parameter name'))
    data_type = models.CharField(max_length=8, help_text=_('Data type'), choices=DATA_TYPE)
    lov_id = models.ForeignKey(Lov, blank=True, null=True, verbose_name=_('list of values'),
                               help_text=_('Link to model List of values'), on_delete=models.CASCADE)
    default_value = models.CharField(max_length=200, verbose_name=_('Default value'), null=True, blank=True)

    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')
        db_table = 'com_parameter'

    def __str__(self):
        return '%s(%s) %s' % (self.param_name, self.name, self.description)
