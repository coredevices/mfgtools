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

class FakeTimer(object):

    TIMERS = []

    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.started = False
        self.expired = False
        self.cancelled = False
        type(self).TIMERS.append(self)

    def __repr__(self):
        state_flags = ''.join([
                'S' if self.started else 'N',
                'X' if self.expired else '.',
                'C' if self.cancelled else '.'])
        return '<FakeTimer({}, {}) {} at {:#x}>'.format(
                self.interval, self.function, state_flags, id(self))

    def start(self):
        if self.started:
            raise RuntimeError("threads can only be started once")
        self.started = True

    def cancel(self):
        self.cancelled = True

    def expire(self):
        '''Simulate the timeout expiring.'''
        assert self.started, 'timer not yet started'
        assert not self.expired, 'timer can only expire once'
        self.expired = True
        self.function()

    @property
    def is_active(self):
        return self.started and not self.expired and not self.cancelled

    @classmethod
    def clear_timer_list(cls):
        cls.TIMERS = []

    @classmethod
    def get_active_timers(cls):
        return [t for t in cls.TIMERS if t.is_active]
