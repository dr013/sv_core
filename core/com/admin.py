from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Dictionary, Parameter, I18n, Lov


class I18nInline(GenericTabularInline):
    model = I18n


class DictionaryAdmin(admin.ModelAdmin):
    list_filter = ('dict_code',)
    list_display = ('dict_code', 'code', 'name', 'dict_val')
    inlines = [
        I18nInline,
    ]


admin.site.register(Dictionary, DictionaryAdmin)


class LovAdmin(admin.ModelAdmin):
    inlines = [
        I18nInline,
    ]


admin.site.register(Lov, LovAdmin)


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('param_name', 'data_type', 'name')
    inlines = [
        I18nInline,
    ]


admin.site.register(Parameter, ParameterAdmin)
