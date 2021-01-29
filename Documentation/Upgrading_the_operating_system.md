# Updating the Raspberry Pi OS

If you are running OTG, you need to make sure you have Internet sharing enabled. See Sharing_your_internet_OTG.md


## Upgrading

For full details see: https://www.raspberrypi.org/documentation/raspbian/updating.md

The summary is:

First, update your system's package list by entering the following command:

    sudo apt update

Next, upgrade all your installed packages to their latest versions with the following command:

    sudo apt full-upgrade

Note that full-upgrade is used in preference to a simple upgrade, as it also picks up any dependency changes that may have been made.

It's worth checking with df -h that you have enough free disk space. The line with /dev/root mounted on / is the key line.


    pi@raspberrypi:~ $ df -h
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/root        15G  1.4G   13G  10% /
    devtmpfs        184M     0  184M   0% /dev
    tmpfs           216M     0  216M   0% /dev/shm
    tmpfs           216M  8.5M  208M   4% /run
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           216M     0  216M   0% /sys/fs/cgroup
    /dev/mmcblk0p1  253M   47M  206M  19% /boot
    tmpfs            44M     0   44M   0% /run/user/1000


## Checking what Operating System you have

    pi@raspberrypi:~ $ uname -a
    Linux raspberrypi 5.4.83+ #1379 Mon Dec 14 13:06:05 GMT 2020 armv6l GNU/Linux

    pi@raspberrypi:~ $ cat /etc/os-release
    PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
    NAME="Raspbian GNU/Linux"
    VERSION_ID="10"
    VERSION="10 (buster)"
    VERSION_CODENAME=buster
    ID=raspbian
    ID_LIKE=debian
    HOME_URL="http://www.raspbian.org/"
    SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
    BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"



