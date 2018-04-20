# Copyright  2018 Eugene Kryukov<ekryukov@icloud.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

from django.conf import settings
from django.db import connection, DatabaseError
from django.utils import translation

logger = logging.getLogger(__name__)
BLANK_LOV = [["", ""], ]


def get_lov_choice(pid):
    csr = connection.cursor()

    sql = "SELECT dict, lov_query FROM com_lov WHERE id = '%s'" % pid
    csr.execute(sql)

    if csr.rowcount == -1:
        return BLANK_LOV

    dict_name, lov_query = csr.fetchone()
    cur_language = translation.get_language()

    if dict_name:
        sql = """
    select dict || code
          , b.text
      from com_dictionary a
         , com_i18n b
         , django_content_type d
         , (select 'LANGENG' as lang
            union all
            select 'LANGRUS') z
     where b.content_type_id = d.id
       and d.model = 'dictionary'
       and b.object_id = a.id
       and b.lang = z.lang
       and b.column_name = 'NAME'
       and b.lang = '%s'
       and a.dict ='%s' """ % (settings.LANG[cur_language.lower()], dict_name)

    else:
        sql = lov_query
    try:
        csr.execute(sql)
        lov = [(o[0], o[1]) for o in csr.fetchall()]
        csr.close()
        return lov
    except DatabaseError as errm:
        error, = errm.args
        logger.error('"Database-Error-Message: %s"' % str(error))
        return BLANK_LOV


def get_dict_choice(dict_name):
    cursor = connection.cursor()
    cur_language = translation.get_language()
    sql = """
    select dict || code
          , b.text
      from com_dictionary a
         , com_i18n b
         , django_content_type d
          ,(select 'LANGENG' as lang
            union all
            select 'LANGRUS') z
     where b.content_type_id = d.id 
       and b.object_id = a.id
       and b.lang = z.lang
       and d.model = 'dictionary'
       and b.column_name = 'NAME'
       and b.lang = '%s'
       and a.dict ='%s'
       """ % (settings.LANG[cur_language.lower()], dict_name)
    try:
        cursor.execute(sql)
        lov = [(o[0], o[1]) for o in cursor.fetchall()]
        cursor.close()
        return lov
    except DatabaseError as errm:
        error, = errm.args
        logger.error('"Database-Error-Message: %s"' % str(error))
        return BLANK_LOV


def get_dict_value():
    cursor = connection.cursor()
    cur_language = translation.get_language()
    sql = """
       select 'DICT', 'DICT - Dictionary'
       union all
       select code, code || ' - ' || b.text  
         from com_dictionary a
            , com_i18n b
            , django_content_type d
             ,(select 'LANGENG' as lang
               union all
               select 'LANGRUS') z
        where b.content_type_id = d.id 
          and b.object_id = a.id
          and b.lang = z.lang
          and d.model = 'dictionary'
          and b.column_name = 'NAME'
          and b.lang = '%s'
          and a.dict ='DICT'
          """ % (settings.LANG[cur_language.lower()])
    try:
        cursor.execute(sql)
        lov = [(o[0], o[1]) for o in cursor.fetchall()]
        cursor.close()
        return lov
    except DatabaseError as errm:
        error, = errm.args
        logger.error('"Database-Error-Message: %s"' % str(error))
        return BLANK_LOV
