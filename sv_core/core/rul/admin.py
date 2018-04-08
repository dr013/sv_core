__author__ = 'Evgeny Kryukov<ekryukov@icloud.com>'

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from com.models import I18n
from .models import NameFormat, Rule, RuleSet, Procedure, Scale, Modifier, ProcedureParameter, ModifierParameter, \
    ParameterValue


class I18nInline(GenericTabularInline):
    model = I18n


class NameFormatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')
    inlines = [
        I18nInline,
    ]


class ModifierAdmin(admin.ModelAdmin):
    list_display = ("pk", "scale", "condition")
    inlines = [
        I18nInline,
    ]


class ScaleAdmin(admin.ModelAdmin):
    list_display = ("pk", "scale_type")
    inlines = [
        I18nInline,
    ]


class ProcedureParameterAdmin(admin.ModelAdmin):
    list_display = ("pk", "proc", "param_name", "is_mandatory", "name")
    inlines = [
        I18nInline,
    ]


class RuleSetAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description", "category")
    inlines = [
        I18nInline,
    ]


admin.site.register(NameFormat, NameFormatAdmin)
admin.site.register(Modifier, ModifierAdmin)
admin.site.register(Scale, ScaleAdmin)
admin.site.register(Rule)
admin.site.register(RuleSet, RuleSetAdmin)
admin.site.register(Procedure)
admin.site.register(ParameterValue)
admin.site.register(ProcedureParameter, ProcedureParameterAdmin)
admin.site.register(ModifierParameter)
