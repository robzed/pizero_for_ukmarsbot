# Information on Raspberry Pi Programming - with Soft Real-time

Real-time on the Pi Zero is tricky without care. We won't get into high preicision timers (standard) or the RT-PREMPT patch (not standard) here - and that's ok because we have the Ardunino Nano to do very fast real-time actions.

However, it's important to consider what might hold up the Raspberry Pi.

The mouse might crash if it doesn’t perform in the correct operation in time, or at least be non-optimal. It’s still possible, without major changes, to convince the Raspberry Pi’s Linux operating system to perform well enough, without special changes (like preemptive kernel threading) or low level drivers.


## SD Card access

If you write to SD card then the program may pause, and the same is true of reading. Try to use only RAM during running the robot and save or load once it’s stopped.


## Real-time threads

Linux by default supports a thread type called real time threads. These are higher priority than normal threads, and it can help get better performance.


**(This is not finished yet)**
