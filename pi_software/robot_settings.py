#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" Main Control file for UKMarsBot Robot with an Arduino Nano co-processor.
    Intended to run on a Raspberry Pi on the actual robot.
"""
#
# Copyright (c) 2016-2021 Rob Probin.
#               (Some items taken from Vison2/Dizzy platform)
# All original work.
#
# This is licensed under the MIT License. Please see LICENSE.
#
# NOTES
# * Coding Convention PEP-8   https://www.python.org/dev/peps/pep-0008/
# * Docstrings PEP-257   https://www.python.org/dev/peps/pep-0257/

from sys import platform
from robot_libs.Raspberry_Pi_Lib import is_raspberry_pi

################################################################
#
# Debug configuration
#

SNOOP_SERIAL_DATA = False        # good but slow
INHIBIT_LOW_BATTERY_SHUTDOWN = False    # stop shutdown. NOTICE: Overriden for Windows, Mac below.
################################################################
#
# Select correct serial port
#    ... usually Raspberry Pi
#        but allows connection of Arduino Nano directly to computer for testing
#
# For Raspberry Pi this shoudl work 'out-of-the-box', but for other platforms
# you'll need to adjust the serial report depending on where the Nano got
# attached...
if platform == "linux" or platform == "linux2":
    if is_raspberry_pi():
        # Raspberry Pi Serial Port
        #
        # See this for full details:
        #
        # https://www.raspberrypi.org/documentation/configuration/uart.md
        #
        # On the Raspberry Pi, one UART is selected to be present on GPIO 14 (transmit)
        # and 15 (receive) - this is the primary UART. By default, this will also be the
        # UART on which a Linux console may be present. Note that GPIO 14 is pin 8 on the
        # GPIO header, while GPIO 15 is pin 10.
        #
        #
        # Model                 first PL011 (UART0)     mini UART
        # Raspberry Pi Zero     primary                 secondary
        # Raspberry Pi Zero W  secondary (Bluetooth)     primary
        #
        # Linux device     Description
        # /dev/ttyS0       mini UART
        # /dev/ttyAMA0     first PL011 (UART0)
        # /dev/serial0     primary UART
        # /dev/serial1     secondary UART
        #
        # Note: /dev/serial0 and /dev/serial1 are symbolic links which point to either
        # /dev/ttyS0 or /dev/ttyAMA0.

        #  primary UART om pins 8 & 10 (GPIO14/15)
        serial_port = "/dev/serial0"

    else:
        # Desktop Linux Machine
        serial_port = "/dev/ttyS1"
        serial_port = "/dev/ttyUSB0"

elif platform == "darwin":
    # OS X - Mac Serial port
    #serial_port = "/dev/cu.usbserial-1420"
    #serial_port = "/dev/cu.usbserial-1410"
    serial_port = "/dev/cu.usbserial-14240"
    INHIBIT_LOW_BATTERY_SHUTDOWN = True

elif platform == "win32":
    # Windows...
    serial_port = "COM3"  #  select your Windows serial port here
    INHIBIT_LOW_BATTERY_SHUTDOWN = True

else:
    raise ValueError("Unknown platform")


################################################################
#
# Constants
#

# Set this to a resonable value
BATTERY_VOLTAGE_TO_SHUTDOWN = 6.5   # volts

# the default values for the front sensor when the robot is backed up to a wall
FRONT_REFERENCE = 44
# the default values for the side sensors when the robot is centred in a cell
LEFT_REFERENCE = 38
RIGHT_REFERENCE = 49

# the values above which, a wall is seen
FRONT_WALL_THRESHOLD = FRONT_REFERENCE / 20  # minimum value to register a wall
LEFT_WALL_THRESHOLD = LEFT_REFERENCE / 2     # minimum value to register a wall
RIGHT_WALL_THRESHOLD = RIGHT_REFERENCE / 2   # minimum value to register a wall


