from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from core.com.models import I18n
from .models import Event, EventObject, EventType, Subscriber, EventRuleSet


class I18nInline(GenericTabularInline):
    model = I18n


class EventAdmin(admin.ModelAdmin):
    list_filter = ('event_type',)
    list_display = ('event_type', 'name')
    inlines = [
        I18nInline,
    ]


class EventTypeAdmin(admin.ModelAdmin):
    list_filter = ('event_type',)
    list_display = ('event_type', 'event_type_raw', 'entity_type')


admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(EventObject)
admin.site.register(Subscriber)
admin.site.register(EventRuleSet)
