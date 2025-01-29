# SPDX-FileCopyrightText: Copyright (c) 2025 Noel Anderson
#
# SPDX-License-Identifier: Unlicense

import time

import board

from fs3000 import FS3000_1015

i2c = board.I2C()  # uses board.SCL and board.SDA

# Example usage
sensor = FS3000_1015(i2c)


while True:
    print(f"Airflow: {sensor.airflow()} m/s")
    time.sleep(2)
