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

from .. import PebbleCommander, exceptions, parsers


@PebbleCommander.command()
def battery_force_charge(cmdr, charging=True):
    """ Force the device to believe it is or isn't charging.
    """
    if parsers.str2bool(charging):
        charging = "enable"
    else:
        charging = "disable"
    ret = cmdr.send_prompt_command("battery chargeopt %s" % charging)
    if ret:
        raise exceptions.PromptResponseError(ret)


@PebbleCommander.command()
def battery_status(cmdr):
    """ Get current battery status.
    """
    return cmdr.send_prompt_command("battery status")
