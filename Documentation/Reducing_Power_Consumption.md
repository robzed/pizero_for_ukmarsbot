# Reducing Power Consumption

## Basic Options

To quote from https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy

| Technique | Power Saved | Notes |
| -- | -- | -- |
| Disable HDMI | 25mA | If you're running a headless Raspberry Pi, there's no need to power the display circuitry, and you can save a little power by running /usr/bin/tvservice -o (-p to re-enable). Add the line to /etc/rc.local to disable HDMI on boot. |
| Disable LEDs | 5mA per LED | If you don't care to waste 5+ mA for each LED on your Raspberry Pi, you can disable the ACT LED on the Pi Zero.|
| Minimize Accessories | 50+ mA | Every active device you plug into the Raspberry Pi will consume some energy; even a mouse or a simple keyboard will eat up 50-100 mA! If you don't need it, don't plug it in. |
| Be Discerning with Software | 100+ mA |  If you're running five or six daemons on your Raspberry Pi, those daemons can waste energy as they cause the processor (or other subsystems) to wake and use extra power frequently. Unless you absolutely need something running, don't install it. Also consider using more power-efficient applications that don't require a large stack of software (e.g. LAMP/LEMP or LEMR) to run.|



## Detail

Disable HDMI saves 25mA



You can also disable the ACT LED … but this seems to be useful to spot shutdown and other SD card operations - It’s only 5mA. In my opinion it's not worth it.

“sudo raspi-config” option 1: System Options.

**(This is not finished yet)**


