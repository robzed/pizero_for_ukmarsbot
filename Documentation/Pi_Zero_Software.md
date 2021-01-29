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

# Setup Python serial library

We will use Python 3 here. If you try to import serial you will probably get an error:

    python3
    pi@raspberrypi:~ $ python3
    Python 3.7.3 (default, Jul 25 2020, 13:03:44) 
    [GCC 8.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import serial
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ModuleNotFoundError: No module named 'serial'
    >>> quit()

So you'll need to install it for Python 3. Let's do it via pip3. You need network access - so if you are just using on the OTG you need to make sure you have network access. There is information here [Sharing the Internet via OTG](Documentation/Sharing_your_internet_OTG.md)

    sudo apt-get install python3-pip

Then install pyserial

    sudo pip3 install pyserial

Then:

    pi@raspberrypi:~ $ python3
    Python 3.7.3 (default, Jul 25 2020, 13:03:44) 
    [GCC 8.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import serial
    >>> port = serial.Serial("/dev/serial0", baudrate = 115200, timeout = 0.1)
    >>> print(port)
    Serial<id=0xb6687d10, open=True>(port='/dev/serial0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=0.1, xonxoff=False, rtscts=False, dsrdtr=False)
    >>> port.inWaiting()
    0


If you have a problem accessing the serial, you might need to give the 'pi' user access - the group is 'dialout'. You can check with the groups command. 

    pi@raspberrypi:~ $ groups
    pi adm dialout cdrom sudo audio video plugdev games users input netdev gpio i2c spi

You can add the 'pi' to the group with:

    sudo adduser pi dialout

For other users replace pi with the user name. 




**(This is not finished yet)**

