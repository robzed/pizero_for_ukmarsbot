# Powering the Pi Zero

We will power the Pi Zero with 5 volts. The Arduino Nano itself has 5v regulator part number LM1117IMPX-5.0 for the new ones (v3), **Does this have enough additional current to power the Pi?**  Notice some third-party Nano’s use the AM1117-5.0, so we will consider that as well (this is a similar part). 

This is a _linear_ regulator - so the power dissipation is higher when the input voltage is bigger, and it needs to be at least 6.3v for higher currents, otherwise the regulator will start dropping out.

Older Arduino Nano’s used a different regulator - part number UA78M05 - this required 7v input minimum before it stopped regulating properly, and additionally might have different power dissipation. No calculation has been done here.


## Current into the Pi Zero at 5v

The average current of the Pi Zero v1.3 running command line with no GUI, with nothing connected and the HDMI disabled is about 100mA @ 5v, although it might higher on boot - we should assume at least twice that to be safe. It’s possible to reduce that to 80mA by for instance, disabling HDMI.

Please see '[Reducing Power Consumption](Reducing_Power_Consumption.md)' for other details.

Powering the Raspberry Pi Zero doesn’t need to be via the PWR IN Micro-USB power-  we can do this via the 40 way header - pins 2 and 4 are connected to the 5v rail. (Obviously we need to connect the ground / 0v pins as well).


## Calculating the power available for the Raspberry Pi from the Ardunio regulator:

Total current **theoretically** available using LM1117IMPX-5.0 = 800mA

Total power **theoretically** available using AM1117-5.0 = 1A

However, the limiting factor is the power dissipation of the package. Since they are linear regulators they get rid of the ‘extra voltage’ (actually extra power) by dissipating it as heat. If you run your UKMARSbot with a Nickel Metal Hydride 9v battery, then it might (when fully charged) sit at 9v (on load, offload it can be higher) - although normally it's about 8.5v. To get down to 5v involves getting rid of all 4v times the current in heat. This is because P = IV (Power equals current times voltage).

The current of the Arduino is probably something like 33mA@5v (or 167mW), but we also need to take account of all 5v and 3v3 usage of the UKMARSBot. This adds up to about 49 mA to 66mA depending upon LEDs @ 5v. (The Arduino can theoretically use I/O to up 233.4mA as well, and we have to assume you don’t leave the IR LEDs on all the time…)

https://arduino.stackexchange.com/questions/926/what-is-the-maximum-power-consumption-of-the-arduino-nano-3-0

The currents looks well within the limits of the 5v regulator - even during boot up, but we also need to consider power dissipation. 

The LM1117 data sheet has a graph  “Figure26. Maximum Allowable Power Dissipation vs Ambient Temperature for SOT-223”. If the ambient temperature is 25 degrees C, then we can get between 800mW and 1.4W depending upon how good the heat sink created by ground plane  - and usually it’s not as good!

At 800mW, dissipating 4v (worst case) at 100mA for the  Pi Zero (Let’s ignore the initial boot up current - and assume the regulator will take a while to get up to 125 degrees C), and then 66mA for the Ardunio and I/O, sensors, etc. 

So 166mA * 4v = 664mW. This gives us some margin (20%) assuming that the power dissipation of the package on this PCB is 800mW. 

NOTICE: The regulator part (which is located on the underside of the Arduino Nano) might get hot at this current - and care should be taken to avoid getting burnt - but usually it’s out of reach when plugged into the UKMarsBOT.


## Other Power notes

The Pi Zero v1.3 has a PAM2306AYPKE, which is a buck regulator for 1.8V/3.3V. Buck regulators are quite efficient (to up 96%) and this means lower currents. NOTE: Earlier Raspberry Pi’s had linear regulators - and these will lead to higher currents. 

Other peripherals (cameras, keyboards, mice, etc.) will greatly increase power usage and current drawn. Do not connect cameras and record video! https://raspi.tv/2017/how-much-power-does-pi-zero-w-use


## IMPORTANT NOTE

If you want to use more features on the Pi Zero, or a Pi Zero W (and Bluetooth from computer and mobile phone is cool, as is a network) - then you will need to calculate whether there is enough current avaialble at 5v, or add a second regulator.

