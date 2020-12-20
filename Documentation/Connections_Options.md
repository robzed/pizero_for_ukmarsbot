# Communication between the micros

**IMPORTANT NOTE:** The Arduino Nano is 5v I/O and the Raspberry Pi is 3v I/O. Care needs to be taken when connecting one to another.

## Option 1 - UART serial lines

Serial: 0 (RX) and 1 (TX). Used to receive (RX) and transmit (TX) TTL serial data. These pins are connected to the corresponding pins of the FTDI USB-to-TTL Serial chip. However, there is a 1 Kohm connection, and so these signals can be overridden by other uses.

Some UKMARS users have this also used for debugging in real-time via a Bluetooth module. This will not be possible if we use these serial lines to talk to the Pi Zero.


## Option 2 - I2C Interface

This is a two wire protocol, which is tracked to A4/A5 and then to  sensor boards, but unused on the current v1 sensor boards. 

However using this interface would step the ability to connect advanced sensor boards using I2C or other analogue inputs.


## Option 3 - SPI Interface

This is tracked to D10, D11, D12, D13. These are mostly used for other functions on the UKMARSBot which don’t make them ideal. A considerable amount of changes would be required - therefore this is discounted from this guide. Adventurous experimenters might consider this interface, however.


## Option 4 - USB interface

This uses the Raspberry Pi as the host interface, and the Arduino nano as the device / peripheral.

This is a reasonable approach - but I have questions about power (the Arduino has power, the Raspberry Pi doesn’t - so maybe a separate power connection needs to be made. Additionally reprogramming the Arduino either need to be done via the Raspberry Pi, or the connection must be disconnected.

A third issue is that connecting to the Raspberry Pi would also use this port in OTG mode.


## Conclusion

Because the Raspberry Pi and Arduino Nano UART serial port is free, except for programming, and both ends are easy to debug on a PC without extra tools, this is the approach we will take.

NOTE: Without somehting like Bluetooth from the Arduino Nano, any debug data will need to be transmitted to the Raspberry Pi - however, since it has quite a lot of memory, we can store it in the Raspberry Pi RAM (then write to SD card after the robot has completed it's real-time movements).

## Things we need to take care of:

1. Ensure that we can still program the Arduino when required via the USB interface (that still uses this UART serial inter
2. We need to be careful how we power off the mouse, or we will need to write-protect the SD card after initial boot (can be done from software) - otherwise the SD card will become corrupt.
3. Ensure that the 5v transmit line of the Arduino doesn’t damage the Raspberry Pi. 
4. Disable the Raspberry Linux Pi console UART so that doesn't interfer with our communication.
5. Provide a communication protocol between the two devices.

