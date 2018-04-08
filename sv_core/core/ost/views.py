#!/usr/bin/env python
#-*- coding:utf-8 -*-

# System
import logging

# Django
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
# App
from ost.models import Instance, Server
from acm.models import Empl

# Logger
logger = logging.Logger(__name__)


@login_required
@cache_page(60 * 60)
def db_instance(request):
    task = []
    instance = Instance.objects.filter(instance_type__instance_type='ISTPORCL').order_by('name')
    return render_to_response('db_instance.html', locals(), context_instance=RequestContext(request))


@login_required
@cache_page(60 * 60)
def server_list(request):

    return render_to_response('servers.html', locals(), context_instance=RequestContext(request))


@login_required
@cache_page(60 * 60)
def server_list_json(request):
    empl = Empl.objects.get(user=request.user)

    if 'page' in request.GET:
        current_page = int(request.GET['page'])
    else:
        current_page = 1

    if 'rows' in request.GET:
        page_rows = int(request.GET['rows'])
    else:
        page_rows = 20
    # servers = Server.objects.all()

    servers = Server.objects.filter(inst=empl.inst)

    total_records = servers.count()
    total_page = int(round(float(total_records) / page_rows))

    return render_to_response('servers.json', locals(), context_instance=RequestContext(request),
                              content_type='application/json')


@cache_page(60 * 60)
def release_index(request):
    return None