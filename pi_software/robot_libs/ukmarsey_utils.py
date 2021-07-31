#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" UKMarsBot Robot Utilities """
#
# Copyright (c) 2020/2021 Rob Probin.
#
# All original work.
#
# This is licensed under the MIT License. Please see LICENSE.
#
# NOTES
# * Coding Convention PEP-8   https://www.python.org/dev/peps/pep-0008/
# * Docstrings PEP-257   https://www.python.org/dev/peps/pep-0257/

import time
import robot_settings

################################################################
#
# Functions
#

def wait_for_button_press(commands):
    """
    Wait for someone to press and release the button. 
    While we are doing this we flash the LED.

    :return: Switch status as a number
    """
    time_to_sleep = 0.02
    time_to_recognise_press = 0.1
    time_to_recognise_release = 0.1
    led_flash_time = 0.5
    count_to_recognise_press = time_to_recognise_press / time_to_sleep
    count_to_recognise_release = time_to_recognise_release / time_to_sleep
    count_led_flash_time = led_flash_time / time_to_sleep

    # wait for switch to be held consistently
    count = 0
    led_count = 0
    while count < count_to_recognise_press:
        state = commands.get_switches()
        if state == 16:
            count += 1
        else:
            count = 0
            # TODO: Make this have different LED displays, e.g. fade, all-flash, etc. 
            # TODO: LED display manager (e.g. for waiting for button, shutting down, etc.)
            led_count += 1
            commands.change_arduino_led(led_count > (
                count_led_flash_time/2) if 1 else 0)
            # TODO: move these output lines to sensor readings
            commands.write_GPIO_output(6, led_count > (
                count_led_flash_time/2) if 1 else 0)
            commands.write_GPIO_output(11, led_count > (
                count_led_flash_time/2) if 1 else 0)

            if led_count > count_led_flash_time:
                led_count = 0
        time.sleep(time_to_sleep)

    # wait for switch to be released for a time
    count = 0
    while count < count_to_recognise_release:
        state = commands.get_switches()
        if state != 16:
            count += 1
        else:
            count = 0
        time.sleep(time_to_sleep)

    return state


WARN_TIME = 10  # seconds
next_warn_time = None

def battery_check(commands):
    ''' read the battery and check if it's low. If it's low, shutdown ''' 
    global next_warn_time
    
    bat_voltage = commands.get_battery_voltage()
    # TODO: Make it indicate when the voltage is starting to get lower (e.g. LED display)
    if bat_voltage < robot_settings.BATTERY_VOLTAGE_TO_SHUTDOWN:
        if next_warn_time is None or time.time() > next_warn_time:
            next_warn_time = time.time()+WARN_TIME
            print("WARNING: Low Voltage", bat_voltage)
        # make it indicate when it is going to shut down? (all-flash?)
        commands.low_battery_shutdown(bat_voltage)
    else:
        next_warn_time = None
    # TODO: Make a periodic battery check
    # TODO: store battery voltage locally, so we don't read it more often than we need to if we are reading it periodically
    # TODO: Should periodic actions be via a timer queue system? (one shot or repeated)
    return bat_voltage



RIGHT_LED_GPIO = 6
LEFT_LED_GPIO = 11
        
def setup_left_and_right_sensor_LEDs(commands):
    ''' configure the led and right LEDs on the sensor board '''

    commands.configure_GPIO_pinmode(RIGHT_LED_GPIO, "OUTPUT")
    commands.configure_GPIO_pinmode(LEFT_LED_GPIO, "OUTPUT")
    
def change_left_sensor_led(commands, state):
    commands.write_GPIO_output(LEFT_LED_GPIO, state)

def change_right_sensor_led(commands, state):
    commands.write_GPIO_output(RIGHT_LED_GPIO, state)
    


def wait_for_front_sensor(commands, delay=time.sleep):
    ''' wait for hand to be waved in front of sensor '''
    commands.enable_sensors()
    delay(0.01)
    
    while commands.front_wall_sensor() < 250:
        delay(0.01)

    while (commands.front_wall_sensor() > 200):
        delay(0.01)

    commands.disable_sensors(commands)
    
    delay(0.5)

