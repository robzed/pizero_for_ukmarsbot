# Logging into the PI

Obviously you could connect to the Raspberry Pi with a monitor, keyboard and mouse - but this is a bit pain.

Since we’ve used the UART for communication to the Ardunio Nano, we can’t log in via serial either.

However, the Pi Zero (only) supports OTG mode, where you can connect it directly to the USB of your computer and access via SSH or VNC. To do this you need to prepare the SD card before you boot it:

For this method, alongside your Pi Zero you will require:
 - MicroUSB cable (USB-A one end to insert into your computer, micro-USB another - to insert into the Pi Zero),
 - MicroSD card (that you programmed with Raspberry Pi OS),
 - a computer which can be running Windows (with Bonjour, iTunes or Quicktime installed), Mac OS or Linux (with Avahi Daemon installed, for example Ubuntu has it built in).

Then do the following:

1. Once Raspbian is flashed, open up the boot partition (in Windows Explorer, Finder etc) and add to the bottom of the 'config.txt' file dtoverlay=dwc2 on a new line, then save the file.
2. If using a recent release of Jessie (Dec 2016 onwards), then create a new file simply called ssh in the SD card as well. By default SSH is now disabled so this is required to enable it. Remember - Make sure your file doesn't have an extension (like .txt etc)!
3. Finally, open up the cmdline.txt. Be careful with this file, it is very picky with its formatting! Each parameter is seperated by a single space (it does not use newlines). Insert modules-load=dwc2,g_ether after rootwait. To compare, an edited version of the cmdline.txt file at the time of writing, can be found in the references below.
4. That's it, eject the SD card from your computer, put it in your Raspberry Pi Zero and connect it via USB to your computer. It will take up to 90s to boot up (shorter on subsequent boots). It should then appear as a USB Ethernet device. You can SSH into it using raspberrypi.local as the address.

## Some references:
- https://gist.github.com/gbaman/975e2db164b3ca2b51ae11e45e8fd40a
- https://blog.gbaman.info/?p=791
- https://raspberrypi.stackexchange.com/questions/38827/how-to-connect-raspberry-pi-zero-to-pc#38828
- https://www.novaspirit.com/2016/10/18/raspberry-pi-zero-usb-dongle/


If you are using *Windows*, you’ll need to install Bonjour.

You can connect to the Rasberrry with a USB cable with a microUSB end plugged into the USB Pi Zero connection (NOT PWR IN). NOTE: Make sure it’s a data cable, not just a charge cable. (One way to test this is to use a Android phone with the cable …)

Because of Bonjour, you can probably directly SSH into the Pi Zero.


More information here especially about Windows: https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/ethernet-gadget

To SSH into your Raspberry Pi you can do this on Linux and Mac

    ssh pi@raspberrypi.local

On Windows, you can use any program that supports SSH, for example Putty, WinSCP, or Teraterm. The address should be raspberrypi.local and the user is 'pi'. 

Password will be default **raspberry**

NOTE: It will give you a warning, since we are using the default password.

The time and date will not be set. If this bugs you, type:

    sudo date -s "6 Dec 2020 22:36"

If the board gets network access, then NTP will synchronise the time.

