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
def reset(cmdr):
    """ Reset the device.
    """
    cmdr.send_prompt_command("reset")


@PebbleCommander.command()
def crash(cmdr):
    """ Crash the device.
    """
    cmdr.send_prompt_command("crash")


@PebbleCommander.command()
def factory_reset(cmdr, fast=False):
    """ Perform a factory reset.

    If `fast` is specified as true or "fast", do a fast factory reset.
    """
    if parsers.str2bool(fast, also_true=["fast"]):
        fast = " fast"
    else:
        fast = ""

    ret = cmdr.send_prompt_command("factory reset%s" % fast)
    if ret:
        raise exceptions.PromptResponseError(ret)
