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

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, Orlin Dimitrov"
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

import time
import json
from urllib.parse import urlparse

import requests

class PicoIP():

#region Properties

    @property
    def host(self):
        """Returns Host URL of the service.

        Returns:
            str: Host URL of the service.
        """

        return self.__host

    @host.setter
    def host(self, host):
        """Set Host URL of the service.

        Args:
            host (str): Host URL of the service.
        """

        host_no_slash = host

        if host_no_slash.endswith("/"):
            host_no_slash = host_no_slash[:-1]

        self.__host = host_no_slash

    @property
    def timeout(self):
        """Get timeout.

        Returns:
            int: Timeout.
        """

        return self.__timeout

    @timeout.setter
    def timeout(self, timeout):
        """Set timeout.

        Args:
            timeout (int): Timeout.
        """

        self.__timeout = timeout

    @property
    def last_sync(self):
        """Last sync time.

        Returns:
            float: Unix timestamp.
        """

        return self.__last_sync

#endregion

#region Constructor

    def __init__(self, **kwargs):

        __user = None
        """Username
        """

        __password = None
        """Password
        """

        __host = "127.0.0.1"
        """Host address.
        """

        __timeout = 5
        """Communication timeout.
        """

        __last_sync = 0
        """Last sync time.
        """

        __api_get_inputs = "/inputs"

        # Username
        if "user" in kwargs:
            user = kwargs["user"]

            if user is None:
                raise ValueError("E-mail can not be None.")

            if user == "":
                raise ValueError("E-mail can not be empty string.")

            self.__user = user

        # Password
        if "password" in kwargs:
            password = kwargs["password"]

            if password is None:
                raise ValueError("Password can not be None.")

            if password == "":
                raise ValueError("Password can not be empty string.")

            self.__password = password

        # Host
        if "host" in kwargs:
            host = kwargs["host"]

            if host is None:
                raise ValueError("Host name can not be None.")

            if host == "":
                raise ValueError("Host name can not be empty string.")

            if not self.__url_validate(host):
                raise ValueError(f"Invalid host name: {host}")

            if host.endswith("/"):
                host = host[:-1]

            self.__host = host

        # Host
        if "timeout" in kwargs:
            timeout = kwargs["timeout"]

            if timeout is None:
                raise ValueError("Timeout can not be None.")

            if timeout == "":
                raise ValueError("Timeout can not be empty string.")

            timeout = int(timeout)
            if timeout < 0:
                raise ValueError("Timeout can not be less then 0.")

            self.timeout = timeout

#endregion

#region Private Methods

    def __url_validate(self, x):
        try:
            result = urlparse(x)
            return all([result.scheme, result.netloc])

        except:
            return False

#endregion

#region Public Methods

    def get_inputs(self):

        response_registers = None

        # URI
        uri = self.host + self.__api_get_inputs

        # Headers
        headers = {"Accept": "application/json"}

        # The request.
        response = requests.get(uri, headers={}, data={}, timeout=self.timeout)

        if response is not None:

            # OK
            if response.status_code == 200:

                if response.text != "":

                    response_registers = json.loads(response.text)

                    # Update last successful time.
                    self.__last_sync = time.time()

            else:
                response_registers = None

        else:
            response_registers = None

        return response_registers

    def get_outputs(self):

        pass

    def set_outputs(self, state):

        pass

#endregion
