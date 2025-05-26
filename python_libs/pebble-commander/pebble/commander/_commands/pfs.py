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
def pfs_prepare(cmdr, size):
    """ Prepare for file creation.
    """
    size = int(str(size), 0)
    if size <= 0:
        raise exceptions.ParameterError('size out of range: %d' % size)
    # TODO: I guess catch errors
    ret = cmdr.send_prompt_command("pfs prepare %d" % size)
    if not ret[0].startswith("Success"):
        raise exceptions.PromptResponseError(ret)


# TODO: pfs-write
# Can't do it with pulse prompt :(


@PebbleCommander.command()
def pfs_litter(cmdr):
    """ Fragment the filesystem.

    Creates a bunch of fragmentation in the filesystem by creating a large
    number of small files and only deleting a small number of them.
    """
    ret = cmdr.send_prompt_command("litter pfs")
    if not ret[0].startswith("OK "):
        raise exceptions.PromptResponseError(ret)
    return [ret[0][3:]]
