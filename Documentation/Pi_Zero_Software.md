# Pi Zero Software

# Summary

Jobs need to be split between the Arduino Nano and the Raspberry Pi Zero.

We want to use the Raspberry Pi processing power and large RAM to do as much as possible, but there are some constraints we need to be aware of as we design the software:
 - We don't have instance access to the sensors and motors from the Pi Zero, and this means we need to do fast operations with low latency on the Arduino Nano.
 - We need to make sure that the Raspberry Pi isn't busy which holds up commands to the Arduino Nano.
        - The SD Card especially is slow to read and write and can delay the program.
 - The serial link between the Pi Zero and Nano is slow - and therefore:
    - Introduces latency between sensor data and actions
    - We need to make sure sensor data and commands are as small as possible. (It will be nice to make them human readible, however, for ease of debugging).
 - The basic Nano only has 2 KByte of RAM and 32 KByte of Flash. 
   - (Although the Arduino Nano has 1KByte of EEPROM, it seems useless when we have an SD Card on the Raspberry Pi - as long as we defer writes till after runs.?)
 - The Pi Zero only has a single processor.
 - The UART is full-duplex (can send and receive simulataneously) - and we should leverage this to minimise latency.


# Overview
The Pi Zero needs software to:

 * Talk to the Ardunino and tell it what to do
 * Process information from the Arduino (e.g. batteries, sensors, switches, etc.)
 * Decide when to stop (e.g. when batteries are too low, or we have complete the mission).
 * Decide when to shutdown the Pi Zero.


**(This is not finished yet)**

