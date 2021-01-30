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
# @todo: Run from GUI and from command line .. and auto-detect which one
#
# NOTES
# * Coding Convention PEP-8   https://www.python.org/dev/peps/pep-0008/
# * Docstrings PEP-257   https://www.python.org/dev/peps/pep-0257/

import serial
import time
from sys import platform
from robot_libs.Raspberry_Pi_Lib import is_raspberry_pi
#from collections import deque
#import datetime


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
        
        serial_port = "/dev/serial0"      # primary UART om pins 8 & 10 (GPIO14/15)

    else:
        # Desktop Linux Machine
        serial_port = "/dev/ttyS1"
        serial_port = "/dev/ttyUSB0"

elif platform == "darwin":
    # OS X - Mac Serial port
    serial_port = "/dev/cu.usbserial-1420"
    
elif platform == "win32":
    # Windows...
    serial_port = "COM3"        # select your Windows serial port here
    
else:
    raise ValueError("Unknown platform")


################################################################
# 
# Globals
# 

################################################################
# 
# Constants
# 
NEWLINE = b"\x0A"    # could be "\n" ... but we know only one byte is required

################################################################
# 
# List of Commands
# 
RESET_STATE_COMMAND = b"^" + NEWLINE

CONTROL_C_ETX = b"\x03"      # aborts line
CONTROL_X_CAN = b"\x18"      # aborts line and resets interpreter

################################################################
# 
# List of Responses
# 
RESET_STATE_RETURN = b"RST"

################################################################
# 
# Functions
# 

def do_command(port, command):
    pass

################################################################
# 
# Blocking Command Functions
# These functions block until they receive an ok
# 
def do_ok(port):
    pass

def get_version(port):
    pass

def get_switches(port):
    pass

def get_sensors(port):
    pass

def set_led(port):
    pass

def reset_arduino(port):
    """
    reset_arduino() does the correct things for us to get the Arduino Nano
    back into a known state to run the robot. 

    :param port: serial port, as opened by main
    :return: Nothing returned
    """ 
    port.write(CONTROL_C_ETX)
    time.sleep(0.20)    # wait 20ms
    port.write(CONTROL_X_CAN)
    time.sleep(0.20)

    found = False
    count = 50
    while not found:
        port.write(RESET_STATE_COMMAND)
        time.sleep(0.20)
        # we do simple processing here
        lines = port.readlines()
        print(lines)
        for line in lines:
            if line.startswith(RESET_STATE_RETURN):
                print("Reset arduino")
                found = True
        count -= 1;
        if(count <= 0):
            print("Having problems resetting arduino")
            count = 200

    do_ok(port)
    get_version(port)

def set_up_port():
    """
    reset_arduino() does the correct things for us to get the Arduino Nano
    back into a known state to run the robot. 

    :param port: serial port, as opened by main
    :return: Nothing returned
    """ 
    port = serial.Serial(serial_port, baudrate = 115200, timeout = 0.1)
    time.sleep(0.05)
    bytes_waiting = port.in_waiting
    if bytes_waiting != 0:
        print("Bytes Waiting = ", bytes_waiting)
        incoming = port.read(bytes_waiting)
        print(incoming)
        print("Flushed bytes")
    return port

################################################################
# 
# Main Program
# 
    
def main():
    """ Main function """
    port = set_up_port()
    reset_arduino(port)
    
    #while True:
    #    pass
    print("Completed")

if __name__ == "__main__":
    main()
