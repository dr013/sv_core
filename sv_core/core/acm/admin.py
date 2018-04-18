#!/usr/bin/env python
# django
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import ugettext as _

from sv_core.core.acm.models import Profile, Section, AgentEmpl
# custom
from sv_core.core.com.models import I18n


class I18nInline(GenericTabularInline):
    model = I18n


class EmplModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['user']


class EmployeeInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _('Employee')
    form = EmplModelForm


# Define a new User admin


class UserAdmin(UserAdmin):
    inlines = (EmployeeInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'inst_name']

    def inst_name(self, obj):
        return obj.empl.inst

    inst_name.short_description = 'Group_name'


class SectionAdmin(admin.ModelAdmin):
    inlines = [
        I18nInline,
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(AgentEmpl)
