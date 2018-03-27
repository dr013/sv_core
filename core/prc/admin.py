from django.contrib import admin

from .models import Session


class SessionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'updated_at', 'is_finish')


admin.site.register(Session, SessionAdmin)
