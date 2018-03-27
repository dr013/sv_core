#!/usr/bin/env python
# coding=utf-8
#
# Created by Evgeny Kryukov<krukov@bpcbt.com> at  29.01.15 19:45<br />
# Last changed by Author
#  LastChangedDate::
#  Revision: LastChangedRevision
#  Module:
#  Header
#  @headcom
from django.forms import ModelForm
from .widgets import ContentTypeSelect

from .models import Subscriber
from django.contrib.auth.models import User


class AdminSubscribeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminSubscribeForm, self).__init__(*args, **kwargs)

        try:
            model = self.instance.content_type.model_class()
            model_key = model._meta.pk.name
        except:
            model = User
            model_key = 'id'
        # self.fields['object_id'].widget = ForeignKeyRawIdWidget(rel=ManyToOneRel(model, model_key))
        self.fields['content_type'].widget.widget = ContentTypeSelect('lookup_id_object_id',
                                                                      self.fields['content_type'].widget.widget.attrs,
                                                                      self.fields['content_type'].widget.widget.choices)

    class Meta:
        model = Subscriber
        exclude = []
