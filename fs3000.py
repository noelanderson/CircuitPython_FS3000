# SPDX-FileCopyrightText: Copyright (c) 2025 Noel Anderson
#
# SPDX-License-Identifier: MIT
"""
`fs3000`
================================================================================

CircuitPython driver library for Renesas FS3000 Air Velocity Sensor Module


* Author(s): Noel Anderson

Implementation Notes
--------------------

**Hardware:**

* FS3000 <https://www.renesas.com/en/products/sensor-products/flow-sensors/fs3000-air-velocity-sensor-module>


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice


"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/noelanderson/CircuitPython_FS3000.git"


from adafruit_bus_device import i2c_device
from busio import I2C
from micropython import const

try:
    from typing import Optional
except ImportError:
    pass


# Map raw sensor outputs to m/s values from datasheet figures 2 & 3
# https://www.renesas.com/en/document/dst/fs3000-datasheet
# Store data as tuples (raw_value, mps_value)

_MODEL_1005 = [
    (409, 0),
    (915, 1.07),
    (1522, 2.01),
    (2066, 3.00),
    (2523, 3.97),
    (2908, 4.96),
    (3256, 5.98),
    (3572, 6.99),
    (3686, 7.23),
]

_MODEL_1015 = [
    (409, 0),
    (1203, 2.00),
    (1597, 3.00),
    (1908, 4.00),
    (2187, 5.00),
    (2400, 6.00),
    (2629, 7.00),
    (2801, 8.00),
    (3006, 9.00),
    (3178, 10.00),
    (3309, 11.00),
    (3563, 13.00),
    (3686, 15.00),
]


_FS3000_DEFAULT_I2C_ADDRESS = const(0x28)


class FS3000:
    """
    Base driver for the FS3000 air velocity sensor.
    Do not use directly, but rather use one of the model-specific derived classes
    FS3000_1005 or FS3000_1015

    :param i2c: The I2C bus object.
    :type i2c: I2C
    """

    def __init__(self, i2c: I2C):
        """
        Initializes the FS3000 sensor.

        :param i2c: The I2C bus instance.
        :type i2c: I2C
        """
        self._device = i2c_device.I2CDevice(i2c, _FS3000_DEFAULT_I2C_ADDRESS)
        self._data_points = _MODEL_1005  # Default

    def airflow(self) -> Optional[float]:
        """
        Sensor data in meters per second (m/s).

        :return: Airflow velocity in meters per second, or None if data is invalid.
        :rtype: Optional[float]
        """
        airflow_raw = self._raw_airflow()
        if airflow_raw is None:
            return None  # Handle invalid data

        # Handle edge cases
        if airflow_raw <= 409:
            return 0
        if airflow_raw >= 3686:
            return self._data_points[-1][1]  # Max m/s for the selected range

        # Find the correct interval using a simple loop
        for i in range(len(self._data_points) - 1):
            raw_low, mps_low = self._data_points[i]
            raw_high, mps_high = self._data_points[i + 1]

            if raw_low <= airflow_raw <= raw_high:
                # Perform linear interpolation
                percentage_of_window = (airflow_raw - raw_low) / (raw_high - raw_low)
                return mps_low + (mps_high - mps_low) * percentage_of_window

        return None  # Should not happen, added for safety

    def _raw_airflow(self) -> Optional[int]:
        """
        Reads raw sensor data from the FS3000.

        :return: The raw airflow value (12-bit integer), or None if checksum fails.
        :rtype: Optional[int]
        """
        result = bytearray(5)
        with self._device as i2c:
            i2c.readinto(result)

        sum = 0
        for n in result:
            sum += n

        # Checksum verification
        if sum & 0xFF == 0:
            return ((result[1] & 0b00001111) << 8) + result[2]
        else:
            return None  # Handle invalid data


class FS3000_1005(FS3000):
    """
    FS3000-1005 sensor variant, with airflow range up to 7.23 m/s.

    :param i2c: The I2C bus instance.
    :type i2c: I2C
    """

    def __init__(self, i2c: I2C):
        """
        Initializes the FS3000-1005 sensor.

        :param i2c: The I2C bus instance.
        :type i2c: I2C
        """
        super().__init__(i2c)

        # Select correct raw data to m/s curve for device model
        self._data_points = _MODEL_1005


class FS3000_1015(FS3000):
    """
    FS3000-1015 sensor variant, with airflow range up to 15.00 m/s.

    :param i2c: The I2C bus instance.
    :type i2c: I2C
    """

    def __init__(self, i2c: I2C):
        """
        Initializes the FS3000-1015 sensor.

        :param i2c: The I2C bus instance.
        :type i2c: I2C
        """

        super().__init__(i2c)

        # Select correct raw data to m/s curve for device model
        self._data_points = _MODEL_1015
