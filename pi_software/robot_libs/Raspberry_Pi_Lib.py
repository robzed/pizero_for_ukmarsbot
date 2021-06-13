#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This module is used for Raspberry Pi Specific functions and classes"""
#
# Copyright (c) 2021 Rob Probin.
# All original work.
#
# This is licensed under the MIT License. Please see LICENSE.

import os
import sys

RPI_file = "/sys/firmware/devicetree/base/model"

# https://gpiozero.readthedocs.io/en/stable/api_output.html#buzzer
class buzzer_emulator:
	def __init__(self): #, pin, *, active_high=True, initial_value=False, pin_factory=None):
		pass
	def on(self):
		print("Simulated on")
	def off(self):
		print("Simulated on")
	def beep(self, on_time=1, off_time=1, n=None, background=True):
		print("Simulated beep for", on_time, off_time)

def is_raspberry_pi():
	"""
	Checks a specific file to see this is likely to be a Raspberry Pi.
	Assumes you've checked Linux with sys.platform.
	:return: True is file looks like a Raspberry Pi
	""" 
	if os.path.isfile(RPI_file):
		f = open(RPI_file, "r")
		data = f.read()
		f.close()
		if data.find("Raspberry") != -1:
			return True
	return False


def shutdown_raspberry_pi():
	''' do the right thing to shutdown the Raspberry Pi ''' 
	if is_raspberry_pi():
		exit_code = os.system("sudo poweroff")
		if exit_code != 0:
			print("sudo poweroff failed")
	else:
		print("Shutdown called - but not Raspberry Pi")
	sys.exit(1)

_buzzer = buzzer_emulator() 

def define_gpio_ports():
	if is_raspberry_pi():
		# https://gpiozero.readthedocs.io/en/stable/api_output.html#buzzer
		from gpiozero import Buzzer
		global _buzzer
		_buzzer = Buzzer(25)

def get_buzzer():
	return _buzzer
 