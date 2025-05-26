# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import logging


class TaggedAdapter(logging.LoggerAdapter):
    '''Annotates all log messages with a "[tag]" prefix.

    The value of the tag is specified in the dict argument passed into
    the adapter's constructor.

    >>> logger = logging.getLogger(__name__)
    >>> adapter = TaggedAdapter(logger, {'tag': 'tag value'})
    '''

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['tag'], msg), kwargs
