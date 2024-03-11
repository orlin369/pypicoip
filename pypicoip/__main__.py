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
import traceback

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

def main():

    # Create parser.
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", type=str, default="172.16.100.2", help="Host/IP of the PicoIP.")
    parser.add_argument("--user", type=str, default="admin", help="Username of the PicoIP.")
    parser.add_argument("--password", type=str, default="admin", help="Password of the PicoIP.")
    parser.add_argument("--p3", type=int, default=0, help="Port 3 of the PicoIP.")
    parser.add_argument("--p5", type=int, default=0, help="Port 5 of the PicoIP.")

    # Take arguments.
    args = parser.parse_args()

    with PicoIP(host=args.host, user=args.user, password=args.password) as client:

        if args.p3 is not None:
            client.set_p3(args.p3)

        if args.p5 is not None:
            client.set_p5(args.p5)

        result = []
        result.append(client.get_p3())
        result.append(client.get_p5())
        result.append(client.get_p6())
        result += client.get_adc()

        print(result)

        # state = client.digitalRead(0)
        # print(state)
        # state = client.analogRead(0)
        # print(state)
        # client.digitalWrite(1, 1)
        # print("OK")
        # client.digitalWrite(0, 0)
        # print("OK")

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(traceback.format_exc())
