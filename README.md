# pizero_for_ukmarsbot
Adding a Rapberry Pi Zero onto a UK Mars Bot

![UKMarsBot and Pi Zero](images/ukmarsbot_pizero.jpeg)

# Background
The UKMarsBot is either a maze solver and line follower, designed by the UK Mars and Robotics Society (UKMars). It has a Arduino Nano attached as the standard CPU. 

 - GitHub Project page: https://github.com/ukmars/ukmarsbot
 - UKMars Project page: https://ukmars.org/projects/ukmarsbot/

This project aims to add a Raspberry Pi Zero to that basic design.


# Methods

There are two potential methods of connecting a Raspberry Pi Zero to the UKMARSbot:

1. Produce an adapter board that converts the Pi Zero header to the Arduino Nano footprint, completely replacing the Ardunio Nano. Other things that will need to be take care of:
   - Provide an ADC - potentially with a serial interface like I2C or SPI. 
   - Provide a 5v regulator.
   - Convert the UKMARS I/O to 3v3. This is not overly problematic- - the http://ukmars.org site details this for other boards (like the Arduino Nano 33 BLE).
   - Figure out how to route a PWM signal to the motors for speed control.
2. Connect the Raspberry Pi to the Arduino over a serial interface to the existing Arduino Nano and use the Nano as an I/O processor.

This article will examine the second option since this is the simpler option to construct without a custom PCB.


# Parts required 
  - UKMarsBot - tested working with Arduino Nano
  - Arduino Nano v3 (or equivalent third party Nano)
  - Pi Zero v1.3

We will be using a Pi Zero (not a Pi Zero W which uses more power)


# Table of Contents
  - Powering the Pi Zero … 5v Power … consideration on power
  - Electrical Communication between the micros
  - Summary of Electrical Connections between Pi Zero and Arduino Nano
  - Wiring up the two units
  - Logging into the PI
  - Scripting language for the I/O processor
  - Mechanical Mounting - Mounting the Raspberry Pi Zero onto UKMarsBot
  - Pi Zero or Pi Zero W


