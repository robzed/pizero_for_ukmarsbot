#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This module is used to capture serial data """
#
# Copyright (c) 2016, 2021 Rob Probin.
# All original work.
#
# This is licensed under the MIT License. Please see LICENSE.


################################################################
# 
# Serial_snooper
# 
LF = '\x0A'

class serial_snooper:
    ''' This class can be used to stub-in for serial so that data traffic
    can be captured and printed and saved. Only methods we used have been
    coded - feel free to extend!
    '''
    
    def __init__(self, port):
        self.port = port
        self.data = []
        
    def read(self, num_chars):
        m = self.port.read(num_chars)
        d = ("read", time.time(), m)
        self.data.append(d)
        return m
    
    def readlines(self):
        m = self.port.readlines()
        d = ("read", time.time(), m)
        self.data.append(d)
        return m
    def read_until(self, expected=LF, size=None):
        m = self.port.read_until(expected)
        d = ("read", time.time(), m)
        self.data.append(d)
        return m
        
    def inWaiting(self):
        return self.port.inWaiting()

    @property
    def in_waiting(self):
        return self.port.in_waiting
    
    def write(self, message):
        d = ("write", time.time(), message)
        self.data.append(d)
        return self.port.write(message)

    def print_all(self):
        for e in self.data:
            d, t, data = e
            print(t, d, data)
        self.data = []
                
    """def save_all(self):
    ''' this save function needs fixing, since it uses the old data storage method '''
        now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        serial_snoop_filename = "serial_snoop_%s.txt" % now
        with open(serial_snoop_filename, "a") as f:
            mode = 0
            time = "?"
            is_write = 0
            for e in self.data:
                if mode == 0:
                    is_write = e
                    mode = 1
                elif mode == 1:
                    time = e
                    mode = 2
                else:
                    if is_write:
                        f.write(str(time)+" tx:"+e.encode("hex")+"\n")
                    else:
                        f.write(str(time)+"       rx:"+e.encode("hex")+"\n")
                    mode = 0
            self.data = []
"""


