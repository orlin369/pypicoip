#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

MIT License

Copyright (c) [2023] [Orlin Dimitrov]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import sys
import argparse
import signal
import traceback
import time

from pypicoip.http.client import PicoIP

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2024, Orlin Dimitrov"
"""Copyright holder"""

__credits__ = []
"""Credits"""

__license__ = "MIT"
"""License
@see https://choosealicense.com/licenses/mit/"""

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__status__ = "Debug"
"""File status."""

#endregion

__time_to_stop = False

def interrupt_handler(signum, frame):
    """Interrupt handler.

    Args:
        signum (int): Interrupt signal type (number).
        frame (frame): Frame when this is happened.
    """

    global __time_to_stop

    __time_to_stop = True

def main():

    global __time_to_stop

    # Add signal handler.
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, interrupt_handler)

    # Create timer data.
    t0 = t1 = 0
    dt = 1

    state = 0

    # Create PicoIP object.
    with PicoIP(host="172.16.100.2", user="admin", password="admin") as client:

        # Run the while loop.
        while True:

            # Stop if break.
            if __time_to_stop:
                break

            # Update time.
            t0 = time.time()

            # If time expire.
            if (t0 - t1) >= dt:

                # Update last time.
                t1 = t0

                # State of the animation.
                if state == 0:
                    client.set_p3(0)
                if state == 1:
                    client.set_p3(1)
                if state == 2:
                    client.set_p3(2)
                if state == 3:
                    client.set_p3(4)
                if state == 4:
                    client.set_p3(8)
                if state == 5:
                    client.set_p3(16)
                if state == 6:
                    client.set_p3(32)
                if state == 7:
                    client.set_p3(64)
                if state == 8:
                    client.set_p3(128)

                # Limit the max state.
                if state == 8:
                    state = 0

                # Move one step forward.
                state += 1

        # Clear after the animation.
        client.set_p3(0)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(traceback.format_exc())
