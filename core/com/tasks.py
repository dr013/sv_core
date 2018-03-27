#!/usr/bin/env python
# coding=utf-8
__author__ = 'Evgeny Krukov<ekryukov@icloud.com>'


from celery.task import periodic_task
from celery.schedules import crontab
from django.contrib.sessions.models import Session
from datetime import datetime


@periodic_task(ignore_result=True, run_every=crontab(hour=0, minute=0))
def clean_sessions():
    Session.objects.filter(expire_date__lt=datetime.now()).delete()
