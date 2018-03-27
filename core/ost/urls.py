#!/usr/bin/env python
# coding=utf-8
#  Created by 'Evgeny Kryukov<krukov@bpcbt.com>' at 13.01.14 12:38<br />
#  Last changed by $Author$
#  $LastChangedDate$
#  Revision: $LastChangedRevision$
#  Module: 
#  $Header$
#  @headcom

from django.conf.urls import patterns, url
from ost import views

urlpatterns = patterns('ost.views',
                       #url(r'^$', views.project_index, name='project_index'),
                       url(r'^server.json$', views.server_list_json, name='server_list_json'),
                       url(r'^server/$', views.server_list, name='server_list'),
                       url(r'^instance.json$', views.server_list_json, name='instance_list_json'),
                       url(r'^instance/$', views.db_instance, name='db_instance'),
                       #url(r'^(?P<server>\S+)/release/$', views.release_index, name='release_index'),
                       #  url(r'^(?P<project>\S+)/release/(?P<release_number>\S+)/$', views.release_number,
                       #      name='release_detail'),
                       #url(r'^(?P<project>\S+)/release/(?P<release_number>\S+)/repo-url-redirect$',
                       #    views.release_url_redirect,
                       #    name='release_url_redirect'),
                       #url(r'^(?P<project>\S+)/release/(?P<release_number>\S+)/last_build/repo-url$', views.build_url,
                       #    name='branch_url'),
                       #url(r'^(?P<project>\S+)/release/(?P<release_number>\S+)/last_build/repo-path$',
                       #    views.build_path,
                       #    name='bpanch_path'),
                       )

