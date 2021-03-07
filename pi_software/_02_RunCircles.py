#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
'''

This program spins on the spot and uses the data to calibrate the three
sensors, assuming it's in a U shaped start position of a standard maze cell.

Various robot parameters including the serial port are in robot_settings.py.

Created on 4 Mar 2021

@author: Rob Probin
'''
#
# Copyright (c) 2021 Rob Probin.
#               (Some items taken from Vison2/Dizzy platform 2016)
# All original work.
#
# This is licensed under the MIT License. Please see LICENSE.
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
import math

################################################################
#
# Configuration constants
#

SPEED_TO_CIRCLE = 250    # in mm/s
CIRCLE_DIAMETER = 30        # in mm

################################################################
#
# Functions
#

def robot_run_circles_setup():
    ''' do basic setup '''
    commands = UkmarseyCommands(robot_settings.serial_port, robot_settings.SNOOP_SERIAL_DATA)
    commands.reset_arduino()
    setup_left_and_right_sensor_LEDs(commands)
    return commands

def robot_run_circles_test_main(commands):
    """
    Main robot function 
    """
    bat_voltage = battery_check(commands)
    print("Battery Voltage", bat_voltage, "volts")

    switch_state = wait_for_button_press(commands)

    print("Switches selected as", "{0:04b}".format(switch_state))

    battery_check(commands)
    time.sleep(0.5)
    
    v_speed = SPEED_TO_CIRCLE
    
    # we need to calculate the required angular velocity
    circumference_distance = math.pi * CIRCLE_DIAMETER
    time_to_complete_circumference = circumference_distance / v_speed 
    # literally 360 divided by time
    # e.g. if the speed takes 4 seconds to complete the distance of the circumfrence
    # then we need 360/4, or 90 degrees per second
    w_angular_velocity_in_degrees_per_sec = 360 / time_to_complete_circumference

    # Figure out direction: 
    #  - Switch lowest bit Clear = anticlockwise
    #  - Switch lowest bit Set = clockwise
    if switch_state & 1:
        print("Clockwise")
        w_angular_velocity_in_degrees_per_sec = -w_angular_velocity_in_degrees_per_sec
        change_right_sensor_led(commands, True)
    else:
        print("Anticlockwise")
        change_left_sensor_led(commands, True)
    
    commands.set_speed_and_rotation(v_speed, w_angular_velocity_in_degrees_per_sec)
    
    # Loop where do we something ... 
    while commands.get_switches() != 16:
        time.sleep(0.05)
        battery_check(commands)
    
    commands.stop_motors();
    time.sleep(1)
    print("Completed Circle Test")


def main():
    ''' This captures specific exceptions and cleans up and get's the robot
        running again
    '''
    version_check()
    try:
        commands = robot_run_circles_setup()
        while True:
            robot_run_circles_test_main(commands)
    except InterpreterError as ie:
        print(type(ie), ie)
        # TODO: Recover connection and stop robot
    except SerialSyncError as sse:
        print(type(sse), sse)


if __name__ == "__main__":
    main()
