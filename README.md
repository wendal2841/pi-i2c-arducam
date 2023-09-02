sudo raspi-config

    # Interface Options
    # > Legacy Camera => enable
    # > VNC => enable

* sudo apt-get install python3-pip
*  sudo modprobe i2c-dev

* sudo nano /boot/config.txt


    # under [all]
    dtparam=i2c_arm=on

* sudo reboot
* 
* git clone https://github.com/wendal2841/pi-i2c-arducam.git
* 
* cd pi-i2c-arducam
* python3 FocuserExample.py
* 
* sudo nano /boot/config.txt


    #under [all]
    dtoverlay=ov5647,vcm

* sudo reboot
* 
* libcamera-still -t 0 --tuning-file /usr/share/libcamera/ipa/raspberrypi/ov5647.json
* 
* cd pi-i2c-arducam
* python3 RpiCamera.py