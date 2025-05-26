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
def version(cmdr):
    """ Get version information.
    """
    return cmdr.send_prompt_command("version")


@PebbleCommander.command()
def boot_bit_set(cmdr, bit, value):
    """ Set some boot bits.

    `bit` should be between 0 and 31.
    `value` should be a boolean.
    """
    bit = int(str(bit), 0)
    value = int(parsers.str2bool(value))
    if not 0 <= bit <= 31:
        raise exceptions.ParameterError('bit index out of range: %d' % bit)
    ret = cmdr.send_prompt_command("boot bit set %d %d" % (bit, value))
    if not ret[0].startswith("OK"):
        raise exceptions.PromptResponseError(ret)
