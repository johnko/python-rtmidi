#!/usr/bin/env python
#
# test_midiin_callback.py
#
"""Shows how to receive MIDI input by setting a callback function."""

import sys
import time

import rtmidi
from rtmidi.midiutil import open_midiport


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))


port = int(sys.argv[1]) if len(sys.argv) > 1 else None
midiin, port_name = open_midiport(port)

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    # just wait for keyboard interrupt in main thread
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
