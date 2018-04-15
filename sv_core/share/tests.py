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

from django.test import TestCase
from .common import get_hash


class CommonTestCase(TestCase):
    def setUp(self):
        pass
        # evnt1 = Event.objects.create(event_type="evnttest", is_cached=True)
        # self.id1 = evnt1.id

    def test_get_hash(self):
        for rec in range(1000):
            self.assertGreaterEqual(64, get_hash(rec, 64))
            self.assertGreater(get_hash(rec, 64), 0)

