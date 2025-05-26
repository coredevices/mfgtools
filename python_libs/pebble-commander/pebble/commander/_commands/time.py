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
def set_time(cmdr, new_time):
    """ Set the time.

    `new_time` should be in epoch seconds.
    """
    new_time = int(str(new_time), 0)
    if new_time < 1262304000:
        raise exceptions.ParameterError("time must be later than 2010-01-01")
    ret = cmdr.send_prompt_command("set time %s" % new_time)
    if not ret[0].startswith("Time is now"):
        raise exceptions.PromptResponseError(ret)
    return ret


@PebbleCommander.command()
def timezone_clear(cmdr):
    """ Clear timezone settings.
    """
    ret = cmdr.send_prompt_command("timezone clear")
    if ret:
        raise exceptions.PromptResponseError(ret)
