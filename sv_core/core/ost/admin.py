#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from com.models import I18n
from .models import *


class I18nInline(GenericTabularInline):
    model = I18n


class InstitutionAdmin(admin.ModelAdmin):
    list_filter = ('identity',)
    list_display = ('identity', 'name', 'description')
    inlines = [
        I18nInline,
    ]


class InstanceInline(admin.TabularInline):
    model = Instance


class ParameterValueInline(admin.TabularInline):
    model = InstanceParameterValue


class InstanceAdmin(admin.ModelAdmin):
    list_filter = ('server', 'instance_type')
    inlines = [
        ParameterValueInline
    ]


class ServerAdmin(admin.ModelAdmin):
    list_display = ('address_ip', 'address_name', 'is_local', 'server_name', 'inst')
    list_filter = ('inst', 'is_local')
    inlines = [
        InstanceInline
    ]


class InstanceTypeAdmin(admin.ModelAdmin):
    inlines = [
        I18nInline,
    ]


class InstanceTypeParameterAdmin(admin.ModelAdmin):
    list_filter = ('instance_type',)


admin.site.register(InstanceType, InstanceTypeAdmin)
# admin.site.register(ServerUser)
admin.site.register(InstanceTypeParameter, InstanceTypeParameterAdmin)
admin.site.register(InstanceParameterValue)
admin.site.register(Instance, InstanceAdmin)
# admin.site.register(Repo)
admin.site.register(Server, ServerAdmin)
admin.site.register(Agent)
admin.site.register(Institution, InstitutionAdmin)
