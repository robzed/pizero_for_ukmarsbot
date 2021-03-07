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
    time_to_recognise_press = 0.2
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

