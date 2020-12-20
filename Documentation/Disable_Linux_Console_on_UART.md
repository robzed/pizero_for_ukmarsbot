# Avoiding the Linux Serial Terminal Console

Normally there serial terminal console on pins 8 and 10 can be used to login. This will interfer with the communication to the Nano so must be disabled. 

To disable this the easiest way is to log onto the Raspberry Pi:

Then use raspi-config as follows:
1. Start raspi-config: *sudo raspi-config*.
2. Select option 3 - Interface Options.
3. Select option 6 - Serial Port.
4. At the prompt *'Would you like a login shell to be accessible over serial?'* answer 'No'
5. At the prompt *'Would you like the serial port hardware to be enabled?'* answer 'Yes'
6. Exit raspi-config and reboot the Pi for changes to take effect.

For other methods, see here: https://elinux.org/RPi_Serial_Connection#S.2FW:_Preventing_Linux_from_using_the_serial_port

References
https://www.raspberrypi.org/documentation/configuration/uart.md


