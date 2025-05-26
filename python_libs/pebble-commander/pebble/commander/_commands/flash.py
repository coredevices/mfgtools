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


# TODO: flash-write
# Can't do it with pulse prompt :(

@PebbleCommander.command()
def flash_erase(cmdr, address, length):
    """ Erase flash area.
    """
    address = int(str(address), 0)
    length = int(str(length), 0)
    if address < 0:
        raise exceptions.ParameterError('address out of range: %d' % address)
    if length <= 0:
        raise exceptions.ParameterError('length out of range: %d' % length)
    # TODO: I guess catch errors
    ret = cmdr.send_prompt_command("erase flash 0x%X %d" % (address, length))
    if not ret[1].startswith("OK"):
        raise exceptions.PromptResponseError(ret)


@PebbleCommander.command()
def flash_crc(cmdr, address, length):
    """ Calculate CRC of flash area.
    """
    address = int(str(address), 0)
    length = int(str(length), 0)
    if address < 0:
        raise exceptions.ParameterError('address out of range: %d' % address)
    if length <= 0:
        raise exceptions.ParameterError('length out of range: %d' % length)
    # TODO: I guess catch errors
    ret = cmdr.send_prompt_command("crc flash 0x%X %d" % (address, length))
    if not ret[0].startswith("CRC: "):
        raise exceptions.PromptResponseError(ret)
    return [ret[0][5:]]


@PebbleCommander.command()
def prf_address(cmdr):
    """ Get address of PRF.
    """
    ret = cmdr.send_prompt_command("prf image address")
    if not ret[0].startswith("OK "):
        raise exceptions.PromptResponseError(ret)
    return [ret[0][3:]]
