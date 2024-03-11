#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

MIT License

Copyright (c) [2024] [Orlin Dimitrov]

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

import re
import time
from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth

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

class PicoIP:

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

        self.__user = None
        """Username of device.
        """

        self.__password = None
        """Password of device.
        """

        self.__host = "172.16.100.2"
        """Host address of device.
        """

        self.__timeout = 5
        """Communication timeout.
        """

        self.__last_sync = 0
        """Last sync time.
        """

        self.__api_get_io_state = "/ioreg.js"
        """APi get IO state.
        """

        self.__api_set_io_state = "/iochange.cgi"
        """API set IO state.
        """

        self.__port_p3 = 0
        """Port P3 state.
        """

        self.__port_p5 = 0
        """Port P5 state.
        """

        self.__port_p6 = 0
        """Port P6 state.
        """

        self.__adc = []
        """Port P6 ADC state.
        """

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

            if self.__url_validate(host):
                pass

            elif self.__parse_ipv4_address(host):
                pass

            else:
                raise ValueError(f"Invalid host name: {host}")

            if host.endswith("/"):
                host = host[:-1]

            if not host.startswith("http://"):
                host = "http://" + host

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

#region Implementation of With

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        pass

#endregion

#region Private Methods

    def __parse_ipv4_address(self, ip_string):
        # Regular expression pattern for matching IPv4 addresses
        ipv4_pattern = r"(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)"

        # Match the pattern in the input string
        match = re.search(ipv4_pattern, ip_string)

        if match:
            return match.group(0)  # Return the matched IPv4 address
        else:
            return None  # Return None if no match is found

    def __url_validate(self, x):
        ret_val = False

        try:
            result = urlparse(x)
            ret_val = all([result.scheme, result.netloc])

        except:
            ret_val = False

        return ret_val

    def __get_bit(self, number, bit_index):
        """
        Get the value of a specific bit in an integer.

        Parameters:
            number (int): The integer from which to extract the bit.
            bit_index (int): The index of the bit to retrieve (0-based index from the right).

        Returns:
            int: The value of the specified bit (0 or 1).
        """
        mask = 1 << bit_index  # Create a mask with the desired bit set to 1
        bit_value = (number & mask) >> bit_index  # Extract the specified bit

        return bit_value

    def __set_bit(self, number, bit_index, bit_value):
        """
        Set a specific bit of an integer to a specified value.

        Parameters:
            number (int): The integer whose bit needs to be set.
            bit_index (int): The index of the bit to set (0-based index from the right).
            bit_value (int): The value to set the bit to (0 or 1).

        Returns:
            int: The modified integer with the specified bit set.
        """
        if bit_value not in (0, 1):
            raise ValueError("Bit value must be either 0 or 1")

        mask = 1 << bit_index  # Create a mask with the desired bit set to 1
        if bit_value == 1:
            number |= mask  # Set the bit to 1
        else:
            number &= ~mask  # Set the bit to 0

        return number

    def __update_inputs_state(self):

        # URI
        # http://172.16.100.2/ioreg.js
        uri = self.host + self.__api_get_io_state

        # Set basic authentication.
        basic = HTTPBasicAuth(self.__user, self.__password)

        # The request.
        response = requests.get(uri, auth=basic, headers={}, data={}, timeout=self.timeout)

        if response is not None:

            # OK
            if response.status_code == 200:

                if response.text != "":

                    # Copy data.
                    temp_data = response.text

                    # Remove unused string.
                    temp_data = temp_data.replace("var IO=new Array ", "")
                    temp_data = temp_data.replace("var IS=new Array ", "")
                    temp_data = temp_data.replace("var N=new Array ", "")
                    temp_data = temp_data.replace("(", "")
                    temp_data = temp_data.replace(")", "")

                    # Split by lines.
                    temp_data=temp_data.split("\r\n")

                    # Split by comma.
                    temp_data=temp_data[0].split(",")

                    # Update IO data.
                    self.__port_p3 = int(temp_data[0], base=16)
                    self.__port_p5 = int(temp_data[1], base=16)
                    self.__port_p6 = int(temp_data[2], base=16)

                    # Update ADC data.
                    self.__adc.clear()
                    for item in temp_data[3:11:1]:
                        self.__adc.append(int(item, 16))

                    # Update last successful time.
                    self.__last_sync = time.time()

    def __update_outputs_state(self):

        # URI
        # http://172.16.100.2/iochange.cgi?ref=re-io&01=01&02=F0
        uri = self.host + self.__api_set_io_state

        # Set basic authentication.
        basic = HTTPBasicAuth(self.__user, self.__password)

        # Set arguments.
        params = {"ref":"re-io", "01": f"{self.__port_p3:02X}", "02": f"{self.__port_p5:02X}"}

        # The request.
        response = requests.get(uri, auth=basic, headers={}, data={}, params=params, timeout=self.timeout)

        if response is not None:

            # OK
            if response.status_code == 200:

                # Update last successful time.
                self.__last_sync = time.time()

#endregion

#region Public Methods

    def get_p3(self):
        """Get port P3 state.

        Returns:
            int: Port P3 state.
        """
        self.__update_inputs_state()
        return self.__port_p3

    def get_p5(self):
        """Get port P5 state.

        Returns:
            int: Port P5 state.
        """
        self.__update_inputs_state()
        return self.__port_p5

    def get_p6(self):
        """Get port P6 state.

        Returns:
            int: Port P6 state.
        """
        self.__update_inputs_state()
        return self.__port_p6

    def get_adc(self):
        """Get port P6 ADC stets.

        Returns:
            int: Port P6 ADC states.
        """
        self.__update_inputs_state()
        return self.__adc

    def set_p3(self, value: int):
        """Set port P3 state.

        Args:
            value (int): Value of the P3. 
        """
        if value < 0:
            return

        if value > 255:
            return

        self.__port_p3 = value
        self.__update_outputs_state()

    def set_p5(self, value: int):
        """Set port P5 state.

        Args:
            value (int): Value of the P5. 
        """
        if value < 0:
            return

        if value > 255:
            return

        self.__port_p5 = value
        self.__update_outputs_state()

    def digitalRead(self, index: int):
        """Digital read from particular pin.

        Args:
            index (int): Pin index.

        Returns:
            int: Specified pin state.
        """
        self.__update_inputs_state()

        state = 0

        if 0 <= index <= 7:
            state = self.__get_bit(self.__port_p3, index)

        elif 8 <= index <= 15:
            state = self.__get_bit(self.__port_p5, index)

        elif 16 <= index <= 23:
            state = self.__get_bit(self.__port_p6, index)

        return state

    def analogRead(self, index: int):
        """Analog read from particular pin.

        Args:
            index (int): Pin index.

        Returns:
            int: Specified pin state.
        """
        self.__update_inputs_state()

        state = False

        if 0 <= index <= 7:
            state = self.__adc[index]

        return state

    def digitalWrite(self, index: int, value: bool):
        """Digital write to particular pin.

        Args:
            index (int): Pin index.
            value (int): Pin value.
        """
        if 0 <= index <= 7:
            self.__port_p3 = self.__set_bit(self.__port_p3, index, value*1)

        elif 8 <= index <= 15:
            self.__port_p5 = self.__set_bit(self.__port_p5, index, value*1)

        self.__update_outputs_state()

#endregion
