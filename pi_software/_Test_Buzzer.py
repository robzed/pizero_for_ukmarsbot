#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" The program simply prints some data from the Arduino 
    Nano then quits.
    
    Intended to run on a Raspberry Pi on the actual robot.
        
    The serial port are set from robot_settings.py.
"""
#
# Copyright (c) 2021 Rob Probin.
#               (Some items taken from Vison2/Dizzy platform 2016)
# All original work.
#
# This is licensed under the MIT License. Please see LICENSE.
#
#
# NOTES
# * Coding Convention PEP-8   https://www.python.org/dev/peps/pep-0008/
# * Docstrings PEP-257   https://www.python.org/dev/peps/pep-0257/

from robot_libs.general_utils import version_check
from robot_libs.ukmarsey_commands import UkmarseyCommands
from robot_libs.ukmarsey_commands import InterpreterError, SerialSyncError
from robot_libs.ukmarsey_utils import wait_for_button_press, battery_check
from robot_libs.ukmarsey_utils import setup_left_and_right_sensor_LEDs, change_left_sensor_led, change_right_sensor_led
from robot_libs.Raspberry_Pi_Lib import define_gpio_ports, get_buzzer

import robot_settings
import time

start_time = time.perf_counter()

################################################################
#
# Functions
#

def robot_print_data_setup():
    ''' do basic setup '''
    commands = UkmarseyCommands(robot_settings.serial_port, robot_settings.SNOOP_SERIAL_DATA)
    commands.reset_arduino()
    setup_left_and_right_sensor_LEDs(commands)
    return commands

def robot_print_data_main(commands):
    """
    Main robot function 
    """
    bat_voltage = battery_check(commands)
    print("Battery Voltage", bat_voltage, "volts")

    switch_state = commands.get_switches()
    print("Switches selected as", "{0:04b}".format(switch_state))
            
    print("Complete Print Data")


def main():
    ''' This captures specific exceptions and cleans up and get's the robot
        running again
    '''

    version_check()
    define_gpio_ports()
    #print(time.perf_counter()-start_time)
    
    get_buzzer().on()
    time.sleep(0.2)
    get_buzzer().off()
    time.sleep(1)
    try:
        commands = robot_print_data_setup()
        robot_print_data_main(commands)
        get_buzzer().beep(0.5, 0.5, 5)
        time.sleep(3)
        while get_buzzer().is_active:
            time.sleep(0.1)
        get_buzzer().beep(0.1, 0.1, 5, True)
        time.sleep(1)
        while get_buzzer().is_active:
            time.sleep(0.1)
  
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
