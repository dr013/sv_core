#!/usr/bin/env python
# coding=utf-8
#  Created by 'Evgeny Kryukov<krukov@bpcbt.com>' at 29.11.13 18:04<br />
#  Last changed by $Author$
#  $LastChangedDate$
#  Revision: $LastChangedRevision$
#  Module:
#  $Header$
#  @headcom
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from com.models import I18n
from .models import Notification, Subscriber, SubscribeGroup


class I18nInline(GenericTabularInline):
    model = I18n


class NotificationAdmin(admin.ModelAdmin):
    inlines = [
        I18nInline,
    ]


class SubscriberInLine(admin.TabularInline):
    model = Subscriber


class SubscribeGroupAdmin(admin.ModelAdmin):
    inlines = [
        SubscriberInLine,
    ]


admin.site.register(Notification, NotificationAdmin)
admin.site.register(SubscribeGroup, SubscribeGroupAdmin)
