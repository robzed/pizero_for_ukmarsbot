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
# @TODO: Run from GUI and from command line .. and auto-detect which one
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
# Constants
# 

# Set this to a resonable value
BATTERY_VOLTAGE_TO_SHUTDOWN = 7.0   # volts

# if we don't get this version, then abort!
MINIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION = 1.2
NEWLINE = b"\x0A"    # could be "\n" ... but we know only one byte is required
UKMARSEY_CLI_ENCODING = 'utf8'

################################################################
# 
# Globals
# 

numeric_error_codes = False
echo_on = True

################################################################
# 
# List of Commands
# 
RESET_STATE_COMMAND = b"^" + NEWLINE
SHOW_VERSION_COMMAND = b"v" + NEWLINE
VERBOSE_OFF_COMMAND = b"V0" + NEWLINE
VERBOSE_ON_COMMAND = b"V1" + NEWLINE
ECHO_OFF_COMMAND = b"E0" + NEWLINE
ECHO_ON_COMMAND = b"E1" + NEWLINE
OK_COMMAND = b"?" + NEWLINE
HELP_COMMAND = b"h" + NEWLINE
SWITCH_READ_COMMAND = b"s" + NEWLINE
BATTERY_READ_COMMAND = b"b" + NEWLINE
MOTOR_ACTION_STOP_COMMAND = b"x" + NEWLINE
LED_COMMAND = b"l%i" + NEWLINE
READ_SENSORS_COMMAND = b"S" + NEWLINE
PINMODE_COMMAND = b"P%i=%s" + NEWLINE
DIGITAL_WRITE_COMMAND = b"D%i=%i" + NEWLINE
DIGITAL_READ_COMMAND = b"D%i" + NEWLINE

CONTROL_C_ETX = b"\x03"      # aborts line
CONTROL_X_CAN = b"\x18"      # aborts line and resets interpreter

################################################################
# 
# List of Responses
# 

UNSOLICITED_PREFIX = b"@"
ERROR_PREFIX = b"@Error:"
RESET_STATE_RETURN = b"RST"
OK_RESULT_VERBOSE = b"OK"
OK_RESULT_NUMERIC = ERROR_PREFIX + b"0"


################################################################
# 
# Exceptions
# 

class SoftReset(Exception):
    pass

class ShutdownRequest(Exception):
    pass

class MajorError(Exception):
    pass

class SerialSyncError(Exception):
    pass

################################################################
# 
# General Commad Helper Functions
# 

def do_command(port, command):
    pass

def process_error_code(data):
    print(data)
    raise SerialSyncError("Interpreter Error code returned")

def process_unsolicited_data(data):
    """ This function handles any unsolicited data returns that are made.
    These always start with an @ character
    """
    if data.startswith(ERROR_PREFIX):
        process_error_code(data)
    else:
        # TODO: Process unsolicited data
        print("Unsolicited data unhandled", data)


def blocking_process_reply(port, expected):
    """ This is a generic reply handler, that handles the most common cases of 
    a single expected return"""
    #print("Expecting", expected)
    while True:
        data = port.read_until(expected=NEWLINE)
        #print('blocking_process_reply:', data)
        if data[-1:] == NEWLINE:
            if data.startswith(expected):
                return True
            # check for "@Defaulting Params" type commands
            elif data[0] == UNSOLICITED_PREFIX:
                process_unsolicited_data(data)
            else:
                # TODO: Probably need to handle errors here?
                print(data)
                raise SerialSyncError("Unexpected return data")
        else:
            # TODO: Get a better method than throwing an exception.
            raise SerialSyncError("Newline not found - timeout")
    
    return False

def blocking_get_reply(port):
    """ This is a generic reply handler, that handles the most common cases of 
    getting some result back"""

    while True:
        data = port.read_until(expected=NEWLINE)
        #print('blocking_get_reply:', data)
        if data[-1:] == NEWLINE:
            # check for "@Defaulting Params" type commands
            if data[0] == UNSOLICITED_PREFIX:
                process_unsolicited_data(data)
            else:
                return data # includes the NEWLINE
        else:
            # TODO: Get a better method than throwing an exception.
            raise SerialSyncError("Newline not found - timeout")
    
    return False


def clear_replies(port):
    """ This is a reply handler that ignores replies up to a timeout happens with no newline"""
    while True:
        data = port.read_until(expected=NEWLINE)
        #print("clear_replies", data)
        if NEWLINE in data:
            if data[0] == b"@":
                process_unsolicited_data(data)
        else:
            break
    
    
################################################################
# 
# Blocking Command Functions
# These functions block until they receive an ok (if applicable).
#
# These blocking commands are one way at a time (also called a half-duplex 
# protocol and/or synchronous) and and is slower that possible - because we 
# don't use the both recieve and transmit cable at the same time.
#
# We can send and receive at the same time - because we have both a receive and 
# a transmit cable. 
#
# This send-and-receive is also called asynchronous or full-duplex. However 
# while this second, faster method, this is harder because we have to manage 
# multiple commands at the same time and match the results to the command that
# generated them.
# 
# There are actually a few replies that happen asynchronously (unsolicited 
# by command) but we handle these inside these commands.
#
# Generally blocking commands are much easier to work with - and should be how 
# you start.

def do_ok_test(port):
    """ do_ok_test is a very basic command that always get a reply. Used for connection testing"""
    port.write(OK_COMMAND)
    if(numeric_error_codes):
        blocking_process_reply(port, OK_RESULT_NUMERIC)
    else:
        blocking_process_reply(port, OK_RESULT_VERBOSE)

def get_version(port):
    """ get_version is a very basic command that gets the version. Used for getting the version"""
    port.write(SHOW_VERSION_COMMAND)
    reply = blocking_get_reply(port).rstrip()
    if len(reply) < 2 or reply[:1] != b'v':
        print("Version returned =", reply)
        raise MajorError("Version return not correct")
    version = float(reply[1:].decode(UKMARSEY_CLI_ENCODING))

    if version < MINIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION:
        print("Minimum required", MINIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION)
        MajorError("Version too old for Pi Zero control program")
    return version

def set_echo_off(port):
    """ Send an echo off to supress echoing of the commands back to us.
    This is a special command in that it doesn't care about any replys on purpose
    """
    port.write(ECHO_OFF_COMMAND)
    clear_replies(port)
    global echo_on
    echo_on = False

def set_echo_on(port):
    """ Send an echo on. 
    This is a special command in that it doesn't care about any replys on purpose
    """
    port.write(ECHO_ON_COMMAND)
    clear_replies(port)
    global echo_on
    echo_on = True

def set_numeric_error_codes(port):
    port.write(VERBOSE_OFF_COMMAND) 
    # No reply expected
    global numeric_error_codes
    numeric_error_codes = True

def set_text_error_codes(port):
    port.write(VERBOSE_ON_COMMAND) 
    # No reply expected
    global numeric_error_codes
    numeric_error_codes = False

def get_switches(port):
    """ get_switches """
    port.write(SWITCH_READ_COMMAND)
    reply = blocking_get_reply(port).rstrip()
    return int(reply.decode(UKMARSEY_CLI_ENCODING))


def change_arduino_led(port, state):
    """
    Turn on/off Arduino LED 

    :param port: serial port, as opened by main
    :param state: 0 or 1 for off and on
    :return: Nothing returned
    """
    port.write(LED_COMMAND % state) 
    # No reply expected

def configure_GPIO_pinmode(port, pin, mode):
    ''' Same as Ardunio Pinmode - set the modes of the GPIO pins on the
    Arduino. 
    :param pin = pin number
    :param mode = string "INPUT", "OUTPUT", or "INPUT_PULLUP"
    :return None
    '''
    if mode == "INPUT":
        mode = b"I"
    elif mode == "OUTPUT":
        mode = b"O"
    elif mode == "INPUT_PULLUP":
        mode = b"U"
    else:
        print("Error in configure_GPIO_pinmode - what is ", mode)
        return 
    
    port.write(PINMODE_COMMAND % (pin, mode))

def write_GPIO_output(port, pin, state):
    ''' Similar to digitalWrite on Arduino
    :param pin = pin number
    :param state = 0 or 1
    :return None
    '''
    port.write(DIGITAL_WRITE_COMMAND % (pin, state))

def read_GPIO_input(port, pin):
    ''' Similar to digitalRead on Arduino
    :param pin = pin number
    :return 0 or 1
    '''
    port.write(DIGITAL_READ_COMMAND % pin)
    reply = blocking_get_reply(port).rstrip()
    return int(reply.decode(UKMARSEY_CLI_ENCODING))

def change_sensor_led(port, led, state):
    raise MajorError("Unimplemented") 

def get_battery_voltage(port):
    """ get battery voltage in volts"""
    port.write(BATTERY_READ_COMMAND)
    return float(blocking_get_reply(port).decode(UKMARSEY_CLI_ENCODING))

#sensor_read_count = 0
#sensor_changed_count = 0

def get_sensors(port):
    """ Read the sensors from the robot 
    Returns dark 4 sensors, then 4 sensors illuminated."""
    #global sensor_changed_count
    #global sensor_read_count
    port.write(READ_SENSORS_COMMAND)
    data = blocking_get_reply(port).decode(UKMARSEY_CLI_ENCODING)
    data = data.strip()
    #sensor_read_count += 1
    if data[-1] == "*":
        #sensor_changed_count += 1
        #print("Sensor Changed {0} out of {1}".format(sensor_changed_count, sensor_read_count))
        data = data[:-1]
    data_list = [int(i) for i in data.split(',')]
    return data_list

def emergency_all_stop_command(port):
    raise MajorError("Unimplemented")

################################################################
# 
# Higher Level Functions
# 

def reset_arduino(port):
    """
    reset_arduino() does the correct things for us to get the Arduino Nano
    back into a known state to run the robot. 

    :param port: serial port, as opened by main
    :return: Nothing returned
    """ 
    port.write(CONTROL_C_ETX)
    time.sleep(0.02)    # wait 20ms
    port.write(CONTROL_X_CAN)
    time.sleep(0.02)

    found = False
    count = 50
    while not found:
        port.write(RESET_STATE_COMMAND)
        time.sleep(0.20)
        # we do simple processing here
        lines = port.readlines()
            #print(lines)
        for line in lines:
            if line.startswith(RESET_STATE_RETURN):
                print("Reset arduino")
                found = True
        count -= 1;
        if(count <= 0):
            print("Having problems resetting arduino")
            count = 200

    clear_replies(port)
    set_echo_off(port)
    # make sure echo is off! (Doing it twice just in case)
    set_echo_off(port)
    do_ok_test(port)
    version = get_version(port)
    print("Arduino Nano Software Version = ", version)
    
    set_numeric_error_codes(port)    
    # final tests that things are working ok
    do_ok_test(port)

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


def wait_for_button_press(port):
    """
    Wait for someone to press and release the button. 
    While we are doing this we flash the LED.

    :return: Switch status as a number
    """
    time_to_sleep = 0.02
    time_to_recognise_press = 0.2
    time_to_recognise_release = 0.1
    led_flash_time = 0.5
    count_to_recognise_press = time_to_recognise_press /  time_to_sleep
    count_to_recognise_release = time_to_recognise_release /  time_to_sleep
    count_led_flash_time = led_flash_time / time_to_sleep
    
    # wait for switch to be held consistently
    count = 0
    led_count = 0
    while count < count_to_recognise_press:
        state = get_switches(port)
        if state == 16:
            count += 1
        else:
            count = 0
            led_count += 1
            change_arduino_led(port, led_count > (count_led_flash_time/2) if 1 else 0)
            # TODO: move these output lines to sensor readings
            write_GPIO_output(port, 6, led_count > (count_led_flash_time/4) if 1 else 0)
            write_GPIO_output(port, 11, led_count > (count_led_flash_time/8) if 1 else 0 )

            if led_count > count_led_flash_time:
                led_count = 0
        time.sleep(time_to_sleep)
        
    # wait for switch to be released for a time
    count = 0
    while count < count_to_recognise_release:
        state = get_switches(port)
        if state != 16:
            count += 1
        else:
            count = 0
        time.sleep(time_to_sleep)
        
    return state

    
################################################################
# 
# Main Program
# 
    
def main():
    """ Main function """
    port = set_up_port()
    reset_arduino(port)

    configure_GPIO_pinmode(port, 6, "OUTPUT")
    configure_GPIO_pinmode(port, 11, "OUTPUT")
    
    bat_voltage = get_battery_voltage(port)
    print("Battery Voltage", bat_voltage, "volts")
    if bat_voltage < BATTERY_VOLTAGE_TO_SHUTDOWN:
        print("WARNING: Low Voltage")
        # TODO: We should shutdown!
    
    switch_state = wait_for_button_press(port)

    print("Switches selected as", "{0:04b}".format(switch_state))

    bat_voltage = get_battery_voltage(port)
    print("Battery Voltage", bat_voltage, "volts")
    if bat_voltage < BATTERY_VOLTAGE_TO_SHUTDOWN:
        print("WARNING: Low Voltage")
        # TODO: We should shutdown!

    
    # Loop where do we something ... in this case read the sensors and output 
    # them on the LED
    while get_switches(port) != 16:
        time.sleep(0.01)
        get_sensors(port)

    print("Completed")

if __name__ == "__main__":
    main()
