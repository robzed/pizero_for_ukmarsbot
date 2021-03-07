#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" General utilties
"""
#
# Copyright (c) 2021 Rob Probin.
# All original work.
#
# This is licensed under the MIT License. Please see LICENSE.
#
# NOTES
# * Coding Convention PEP-8   https://www.python.org/dev/peps/pep-0008/
# * Docstrings PEP-257   https://www.python.org/dev/peps/pep-0257/

import sys
from robot_libs.Raspberry_Pi_Lib import is_raspberry_pi
import serial


def version_check():
    # check minimum python version
    print("Python version", sys.version)
    
    # check minimum PySerial verison
    print("PySerial version", serial.VERSION)
    
    # check minimum operation system verison - only applies to Raspberry Pi
    if is_raspberry_pi():
        pass
