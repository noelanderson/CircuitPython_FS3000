Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-fs3000/badge/?version=latest
    :target: https://circuitpython-fs3000.readthedocs.io/
    :alt: Documentation Status



.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/noelanderson/CircuitPython_FS3000/workflows/Build%20CI/badge.svg
    :target: https://github.com/noelanderson/CircuitPython_FS3000/actions
    :alt: Build Status


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython driver library for Renesas FS3000 Air Velocity Sensor Module

Reads airflow in m/s


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.


On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-fs3000/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-fs3000

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-fs3000

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-fs3000

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install fs3000

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    import time
    import board

    from fs3000 import FS3000_1015

    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Example usage
    sensor = FS3000_1015(i2c)


    while True:
        print(f"Airflow: {sensor.airflow()} m/s")
        time.sleep(2)


Documentation
=============

Class Diagram for library

.. figure:: https://raw.githubusercontent.com/noelanderson/CircuitPython_FS3000/refs/heads/main/uml/fs3000.svg
   :alt: Class Diagram


API documentation for this library can be found on `Read the Docs <https://circuitpython-fs3000.readthedocs.io/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/noelanderson/CircuitPython_FS3000/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
