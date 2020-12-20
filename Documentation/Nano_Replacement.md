# Replacing the Arduino Nano entirely with a Pi Zero

This information is provided for information only, and shoudl be considered provisional.

**(This is not finished yet)**


## General approach

It's probably worth creating a daughterboard that connects into the Arduino nano footprint and also allows the 40-way Raspberry Pi header connected. 


## Add link to info about 3v3 change (e.g 74HCxx rather than 74LSxx)

This UKMarsBot v1 was designed to use 5v, however, some work has been made on running it on 3v aleady.


## 5v regulator

The Raspberry Pi Zero requires a 5v supply - which can be provided via one micro USB headers or via the 5v pins on the GPIO header.

Possible options are:
 - DC-DC converter - this is probably the best option


## ADC - Analogue to digital converter



## Add link to info about PWM


## Other notes (add in above)
Provide an ADC - potentially with a serial interface like I2C or SPI.
Provide a 5v regulator.
Convert the UKMARS I/O to 3v3. This is not overly problematic- - the http://ukmars.org site details this for other boards (like the Arduino Nano 33 BLE).
Figure out how to route a PWM signal to the motors for speed control.
