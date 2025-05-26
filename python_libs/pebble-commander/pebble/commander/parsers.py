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

import re

from . import exceptions


def str2bool(s, also_true=[], also_false=[]):
    s = str(s).lower()
    if s in ("yes", "on", "t", "1", "true", "enable") or s in also_true:
        return True
    if s in ("no", "off", "f", "0", "false", "disable") or s in also_false:
        return False
    raise exceptions.ParameterError("%s not a valid bool string." % s)


def str2mac(s):
    s = str(s)
    if not re.match(r'[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}', s):
        raise exceptions.ParameterError('%s is not a valid MAC address' % s)
    mac = []
    for byte in str(s).split(':'):
        mac.append(int(byte, 16))
    return tuple(mac)
