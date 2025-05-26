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

'''Writer for Libpcap capture files

https://wiki.wireshark.org/Development/LibpcapFileFormat
'''

from __future__ import absolute_import

import struct
import threading
import time


LINKTYPE_PPP_WITH_DIR = 204


class PcapWriter(object):

    def __init__(self, outfile, linktype):
        self.lock = threading.Lock()
        self.outfile = outfile
        self._write_pcap_header(linktype)

    def close(self):
        with self.lock:
            self.outfile.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _write_pcap_header(self, linktype):
        header = struct.pack('!IHHiIII',
                             0xa1b2c3d4,  # guint32 magic_number
                             2,  # guint16 version_major
                             4,  # guint16 version_minor
                             0,  # guint32 thiszone
                             0,  # guint32 sigfigs (unused)
                             65535,  # guint32 snaplen
                             linktype)  # guint32 network
        self.outfile.write(header)

    def write_packet(self, data, timestamp=None, orig_len=None):
        assert len(data) <= 65535
        if timestamp is None:
            timestamp = time.time()
        if orig_len is None:
            orig_len = len(data)
        ts_seconds = int(timestamp)
        ts_usec = int((timestamp - ts_seconds) * 1000000)
        header = struct.pack('!IIII', ts_seconds, ts_usec, len(data), orig_len)
        with self.lock:
            self.outfile.write(header + data)
