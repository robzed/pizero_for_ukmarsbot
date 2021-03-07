#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" Sensor test for UKMarsBot Robot with an Arduino Nano co-processor.
    Intended to run on a Raspberry Pi on the actual robot.
    
    This program waits for a button press, then illuminates the 
    three UKMARSBot lefts if an object is brought in close to the sensors. 
    
    The sensitivity and serial port are set from robot_settings.py.
"""
#
# Copyright (c) 2020-2021 Rob Probin.
#               (Some items taken from Vison2/Dizzy platform 2016)
# All original work.
#
# This is licensed under the MIT License. Please see LICENSE.
#
# @TODO: Run from GUI and from command line .. and auto-detect which one
#
# NOTES
# * Coding Convention PEP-8   https://www.python.org/dev/peps/pep-0008/
# * Docstrings PEP-257   https://www.python.org/dev/peps/pep-0257/

from robot_libs.general_utils import version_check
from robot_libs.ukmarsey_commands import UkmarseyCommands
from robot_libs.ukmarsey_commands import InterpreterError, SerialSyncError
from robot_libs.ukmarsey_utils import wait_for_button_press, battery_check
from robot_libs.ukmarsey_utils import setup_left_and_right_sensor_LEDs, change_left_sensor_led, change_right_sensor_led
import robot_settings
import time

################################################################
#
# Functions
#

def robot_sensor_test_setup():
    ''' do basic setup '''
    commands = UkmarseyCommands(robot_settings.serial_port, robot_settings.SNOOP_SERIAL_DATA)
    commands.reset_arduino()
    setup_left_and_right_sensor_LEDs(commands)
    return commands

def robot_sensor_test_main(commands):
    """
    Main robot function 
    """
    bat_voltage = battery_check(commands)
    print("Battery Voltage", bat_voltage, "volts")

    switch_state = wait_for_button_press(commands)

    print("Switches selected as", "{0:04b}".format(switch_state))

    battery_check(commands)

    # Loop where do we something ... in this case read the sensors and output
    # them on the LED
    while commands.get_switches() != 16:
        time.sleep(0.02)
        right, front, left, _, _, _ = commands.get_sensors_faster()
        gFrontWall = front > robot_settings.FRONT_REFERENCE / 4
        gLeftWall = left > robot_settings.LEFT_REFERENCE / 2
        gRightWall = right > robot_settings.RIGHT_REFERENCE / 2
        commands.change_arduino_led(gFrontWall if 1 else 0)
        change_left_sensor_led(commands, gLeftWall if 1 else 0)
        change_right_sensor_led(commands, gRightWall if 1 else 0)

    '''    
        // calculate the alignment error - too far right is negative
        if ((left + right) > (gLeftReference + gRightReference) / 4) {
        if (left > right) {
            gSensorCTE = (left - LEFT_REFERENCE);
            gSensorCTE /= left;
            } else {
          gSensorCTE = (RIGHT_REFERENCE - right);
          gSensorCTE /= right;
            }
          } else {
            gSensorCTE = 0;
          }
          '''
            
    print("Completed Sensor Test")


def main():
    ''' This captures specific exceptions and cleans up and get's the robot
        running again
    '''
    version_check()
    try:
        commands = robot_sensor_test_setup()
        while True:
            robot_sensor_test_main(commands)
    except InterpreterError as ie:
        print(type(ie), ie)
        # TODO: Recover connection and stop robot
    except SerialSyncError as sse:
        print(type(sse), sse)


        # TODO: Recover connection and stop robot
'''        global port_snooper_copy
        port_snooper_copy.print_all()
   '''

if __name__ == "__main__":
    main()
