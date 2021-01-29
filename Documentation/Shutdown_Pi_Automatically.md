# Shutting Down the Raspberry Pi Automatically

If you just turn the switch off the UK Mars Bot, then there is some chance - if it’s written to the SD card (always possible) that you will corrupt the SD card and will need to refresh it. 

Obviously you could plug in a USB cable and issue “sudo shutdown -h now” or “sudo poweroff”, but it’s not very convenient. (Wait for the LED to stop flashing and go out).

It’s much better to read the switches on the UKMARSBot and shutdown the Pi Zero that way - based on the program in the Raspberry Pi. This can either be by the press-button or switches, but also probably needs to be when the battery is low.


