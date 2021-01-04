# Programming the Arduino Nano from the Raspberry Pi Zero

** This is work in progress and has not been tested yet **

You will need an extra GPIO line on the Raspberry Pi, and a schottky diode connected between that GPIO and Pin 3 on the Ardunio Nano. (The alternative is a logic shift gate or a transistor).

We will use Pin 12 which is GPIO 18. This is right next to the serial connections - so we can use one 5 pin header. In fact, in an ideal situation we could use a 7 pin header so that we have two Ground connections and two 5v connections (Pins 2, 4, 6, 8, 10, 12, 14). That will ensure good grounding and power at the raspberry pi end.

(The alternative is another like that can be used as a DTR pin.)

At the UKMARSbot there is no reset at a header - so we will need to solder a wire onto pin 3 of the Arduino Nano and provide our own connection method.


## Theory of operation

When the Raspberry Pi outputs a logic zero, the drop is low enoguh across the schottky diode to pull down the reset and ensure the Arduino resets. That way the Raspberry Pi  can start



*(Add schematic diagram - todo !)*



