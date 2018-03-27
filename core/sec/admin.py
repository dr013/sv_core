from django import forms
from django.contrib import admin

from .models import KeyManage


class KeyManageForm(forms.ModelForm):
    key = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = KeyManage
        exclude = ['created']


class AdminKeyManage(admin.ModelAdmin):
    list_display = ('user', 'valid_till', 'updated', 'key_type')
    form = KeyManageForm


admin.site.register(KeyManage, AdminKeyManage)
