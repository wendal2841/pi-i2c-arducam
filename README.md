* sudo modprobe i2c-dev
* sudo apt-get install python3-pip
* pip3 install opencv-python==4.5.1.48
* sudo apt-get install libatlas-base-dev
* pip3 install --upgrade numpy
* pip3 install pygame
*
* sudo nano /boot/config.txt
* #under [all] 
* dtoverlay=ov5647,vcm 
* dtparam=i2c_arm=on
* 
* cd pi-i2c-arducam
* python3 FocuserExample.py
* python3 TestCamera.py -i 10
* python3 RpiCamera.py