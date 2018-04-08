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
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Abstract base class
class Base(models.Model):
    created_at = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True, editable=False)
    deleted_at = models.DateTimeField(_("Deleted"), blank=True, null=True, editable=False)

    class Meta:
        abstract = True

    @property
    def name(self):
        return "{num:08d}".format(num=self.id)
