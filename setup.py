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

from os import path

from setuptools import setup, find_packages

from sv_core.share.common import get_version

setup(
    name="sv_core",
    version=get_version(),
    author="Eugene Kryukov",
    author_email="ekryukov@icloud.com",
    packages=find_packages(exclude=["manage.py", ]),
    license='APACHE2.0',
    python_requires='>=3',
    long_description=open(path.join(path.dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "django-sequences==2.2",
    ],
    url="https://github.com/dr013/sv_core",
)
