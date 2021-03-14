#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" Main Control file for UKMarsBot Robot with an Arduino Nano co-processor.
    Intended to run on a Raspberry Pi on the actual robot.
"""
#
# Copyright (c) 2020/2021 Rob Probin.
#               (Some items taken from Vison2/Dizzy platform 2016)
# All original work.
#
# This is licensed under the MIT License. Please see LICENSE.
#
# NOTES
# * Coding Convention PEP-8   https://www.python.org/dev/peps/pep-0008/
# * Docstrings PEP-257   https://www.python.org/dev/peps/pep-0257/

import serial
import time
import datetime
from robot_libs.serial_snooper import serial_snooper
from robot_libs.Raspberry_Pi_Lib import shutdown_raspberry_pi
from robot_settings import INHIBIT_LOW_BATTERY_SHUTDOWN

################################################################
#
# Constants - usually not changed
#

# if we don't get this version, then abort!
MINIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION = 1.4
MAXIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION = 1.4    # can be None
NEWLINE = b"\x0A"    # could be "\n" ... but we know only one byte is required
NEWLINE_VALUE = NEWLINE[0]
UKMARSEY_CLI_ENCODING = 'utf8'


################################################################
#
# List of Command Constants
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
READ_SENSORS_HEX_COMMAND = b"Sh" + NEWLINE      # use read Hex (faster)
PINMODE_COMMAND = b"P%i=%s" + NEWLINE
DIGITAL_WRITE_COMMAND = b"D%i=%i" + NEWLINE
DIGITAL_READ_COMMAND = b"D%i" + NEWLINE
SET_SPEED_AND_ROTATION = b"T%i,%i" + NEWLINE
STOP_MOTORS_COMMANDS = b"x" + NEWLINE

CONTROL_C_ETX = b"\x03"      # aborts line
CONTROL_X_CAN = b"\x18"      # aborts line and resets interpreter

################################################################
#
# List of Response Constants
#

UNSOLICITED_PREFIX = b"@"
UNSOLICITED_PREFIX_VALUE = UNSOLICITED_PREFIX[0]
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


class InterpreterError(Exception):
    pass


class UkmarseyCommands:
    """ This is the main control class for commands.
    
    We make this a class so that:
     * Method names are automatially associated with an instance. 
     * Variables are associated with the object
     * It's easy to see what's a private member (starting with _)
    
    The alternative is passing the serial port 
    into each command, and having a long list of imports
    or using from ukmarsey_commands import * which is horrible
    because it polutes the namespace - which increases changes of
    collisions and makes debugging harder.
    
    There will probably never be more than one.
    """
    ################################################################
    #
    # General Commad Helper Functions
    #
    
    
    def _do_command(self, command):
        # TODO: Is this obsolete and can be deleted?
        pass
    
    
    def _process_error_code(self, data):
        print(data)
        raise InterpreterError("Interpreter Error code returned")
    
    
    def _process_unsolicited_data(self, data):
        """ This function handles any unsolicited data returns that are made.
        These always start with an @ character
        """
        if data.startswith(ERROR_PREFIX):
            self._process_error_code(data)
        else:
            # TODO: Process unsolicited data
            print("Unsolicited data unhandled", data)
    
    def _blocking_process_reply(self, expected):
        """ This is a generic reply handler, that handles the most common cases of 
        a single expected return"""
        #print("Expecting", expected)
        while True:
            data = self.port.read_until(NEWLINE)
            #print('_blocking_process_reply:', data)
            if data[-1] == NEWLINE_VALUE:
                if data.startswith(expected):
                    return True
                # check for "@Defaulting Params" type commands
                elif data[0] == UNSOLICITED_PREFIX_VALUE:
                    self._process_unsolicited_data(data)
                else:
                    # TODO: Probably need to handle errors here?
                    print(data)
                    raise SerialSyncError("Unexpected return data")
            else:
                # TODO: Get a better method than throwing an exception.
                raise SerialSyncError("Newline not found - timeout")
    
        return False
    
    
    def _blocking_get_reply(self):
        """ This is a generic reply handler, that handles the most common cases of 
        getting some result back"""
    
        while True:
            data = self.port.read_until(NEWLINE)
            #print('_blocking_get_reply:', data)
            if data[-1] == NEWLINE_VALUE:
                # check for "@Defaulting Params" type commands
                if data[0] == UNSOLICITED_PREFIX_VALUE:
                    self._process_unsolicited_data(data)
                else:
                    return data  # includes the NEWLINE
            else:
                # TODO: Get a better method than throwing an exception.
                raise SerialSyncError("Newline not found - timeout")
    
        return False
    
    
    def _clear_replies(self):
        """ This is a reply handler that ignores replies up to a timeout happens with no newline"""
        while True:
            data = self.port.read_until(NEWLINE)
            #print("_clear_replies", data)
            if NEWLINE in data:
                if data[0] == b"@":
                    self._process_unsolicited_data(data)
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
    
    def do_ok_test(self):
        """ do_ok_test is a very basic command that always get a reply. Used for connection testing"""
        self.port.write(OK_COMMAND)
        if(self.numeric_error_codes):
            self._blocking_process_reply(OK_RESULT_NUMERIC)
        else:
            self._blocking_process_reply(OK_RESULT_VERBOSE)
    
    
    def get_version(self):
        """ get_version is a very basic command that gets the version. Used for getting the version"""
        self.port.write(SHOW_VERSION_COMMAND)
        reply = self._blocking_get_reply().rstrip()
        if len(reply) < 2 or reply[:1] != b'v':
            print("Version returned =", reply)
            raise MajorError("Version return not correct")
        version = float(reply[1:].decode(UKMARSEY_CLI_ENCODING))
    
        if version < MINIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION:
            print("Minimum required", MINIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION)
            MajorError("Version too old for Pi Zero control program")
            
        if MAXIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION is not None:
            if version > MAXIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION:
                print("Maximum required", MAXIMUM_UKMARSEY_ARDUINO_NANO_SOFTWARE_VERSION)
                MajorError("Version too new for Pi Zero control program")
        return version
    
    
    def set_echo_off(self):
        """ Send an echo off to supress echoing of the commands back to us.
        This is a special command in that it doesn't care about any replys on purpose
        """
        self.port.write(ECHO_OFF_COMMAND)
        self._clear_replies()
        self.echo_on = False
    
    
    def set_echo_on(self):
        """ Send an echo on. 
        This is a special command in that it doesn't care about any replys on purpose
        """
        self.port.write(ECHO_ON_COMMAND)
        self._clear_replies()
        self.echo_on = True
    
    
    def set_numeric_error_codes(self):
        self.port.write(VERBOSE_OFF_COMMAND)
        # No reply expected
        self.numeric_error_codes = True
    
    
    def set_text_error_codes(self):
        self.port.write(VERBOSE_ON_COMMAND)
        # No reply expected
        self.numeric_error_codes = False
    
    
    def get_switches(self):
        """ get_switches """
        self.port.write(SWITCH_READ_COMMAND)
        reply = self._blocking_get_reply().rstrip()
        return int(reply.decode(UKMARSEY_CLI_ENCODING))
    
    
    def change_arduino_led(self, state):
        """
        Turn on/off Arduino LED 
    
        :param port: serial port, as opened by main
        :param state: 0 or 1 for off and on
        :return: Nothing returned
        """
        self.port.write(LED_COMMAND % state)
        # No reply expected
    
    
    def configure_GPIO_pinmode(self, pin, mode):
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
    
        self.port.write(PINMODE_COMMAND % (pin, mode))
    
    
    def write_GPIO_output(self, pin, state):
        ''' Similar to digitalWrite on Arduino
        :param pin = pin number
        :param state = 0 or 1
        :return None
        '''
        self.port.write(DIGITAL_WRITE_COMMAND % (pin, state))
    
    
    def read_GPIO_input(self, pin):
        ''' Similar to digitalRead on Arduino
        :param pin = pin number
        :return 0 or 1
        '''
        self.port.write(DIGITAL_READ_COMMAND % pin)
        reply = self._blocking_get_reply().rstrip()
        return int(reply.decode(UKMARSEY_CLI_ENCODING))
    
    
    def change_sensor_led(self, led, state):
        raise MajorError("Unimplemented")
    
    
    def get_battery_voltage(self):
        """ get battery voltage in volts"""
        self.port.write(BATTERY_READ_COMMAND)
        return float(self._blocking_get_reply().decode(UKMARSEY_CLI_ENCODING))
    
    
    def get_sensors(self):
        """ Read the sensors from the robot 
        Returns 6 sensor readings (light-dark) """
        self.port.write(READ_SENSORS_COMMAND)
        data = self._blocking_get_reply().decode(UKMARSEY_CLI_ENCODING)
        data = data.strip()
        data_list = [int(i) for i in data.split(',')]
        return data_list
    
    
    def get_sensors_faster(self):
        """ Read the sensors from the robot 
        Returns 6 sensor readings (light-dark) """
        self.port.write(READ_SENSORS_HEX_COMMAND)
        data = self._blocking_get_reply().decode(UKMARSEY_CLI_ENCODING)
        data = data.strip()
        # multiply by 4 to make consistent with other forms
        data_list = [x*4 for x in list(bytes.fromhex(data))]
        return data_list
    
    def emergency_all_stop_command(self):
        # Control-X
        self.port.write(CONTROL_X_CAN)
        self.port.write(CONTROL_X_CAN)
        self._clear_replies()
    
    def stop_motors(self):
        self.port.write(STOP_MOTORS_COMMANDS)
        
    def set_speed_and_rotation(self, v, w):
        self.port.write(SET_SPEED_AND_ROTATION % (v, w))


    ################################################################
    #
    # Higher Level Functions
    #

    def low_battery_shutdown(self, bat_voltage):
        if not INHIBIT_LOW_BATTERY_SHUTDOWN:
            self.emergency_all_stop_command()
            f = open('shutdown_log.txt', 'a')
            f.write("%s Low Battery Shutdown - %fv\n" % (str(datetime.datetime.now()), bat_voltage))
            f.close()
            shutdown_raspberry_pi()
        
    def reset_arduino(self):
        """
        reset_arduino() does the correct things for us to get the Arduino Nano
        back into a known state to run the robot. 
    
        :param port: serial port, as opened by main
        :return: Nothing returned
        """
        self.port.write(CONTROL_C_ETX)
        time.sleep(0.02)    # wait 20ms
        self.port.write(CONTROL_X_CAN)
        time.sleep(0.02)
    
        found = False
        count = 50
        while not found:
            self.port.write(RESET_STATE_COMMAND)
            time.sleep(0.20)
            # we do simple processing here
            lines = self.port.readlines()
            # print(lines)
            for line in lines:
                if line.startswith(RESET_STATE_RETURN):
                    print("Reset arduino")
                    found = True
            count -= 1
            if(count <= 0):
                print("Having problems resetting arduino")
                count = 200
    
        self._clear_replies()
        self.set_echo_off()
        # make sure echo is off! (Doing it twice just in case)
        self.set_echo_off()
        self.do_ok_test()
        version = self.get_version()
        print("Arduino Nano Software Version = ", version)
        self._clear_replies()   # clear ok from get version

        self.set_numeric_error_codes()
        # final tests that things are working ok
        self.do_ok_test()
    
    
    ################################################################
    #
    # Set up Functions
    #
    
    def set_up_port(self):
        """
        reset_arduino() does the correct things for us to get the Arduino Nano
        back into a known state to run the robot. 
    
        :param port: serial port, as opened by main
        :return: Nothing returned
        """
        port = serial.Serial(self.serial_port, baudrate=self.baud_rate, timeout=0.1)
        if self.snoop_serial_data:
            port = serial_snooper(port)
        self.port = port

        time.sleep(0.05)

        bytes_waiting = self.port.in_waiting
        if bytes_waiting != 0:
            print("Bytes Waiting = ", bytes_waiting)
            incoming = self.port.read(bytes_waiting)
            print(incoming)
            print("Flushed bytes")
            
        return port
    
    def __init__(self, serial_port = None, snoop_serial_data = False, baud_rate = 115200):
        """ Init the instance. """
        self.serial_port = serial_port
        self.snoop_serial_data = snoop_serial_data
        self.baud_rate = baud_rate

        if serial_port is not None:
            self.set_up_port()
        else:
            self.port = None
            
        self.numeric_error_codes = False
        self.echo_on = True
