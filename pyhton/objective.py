# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 15:45:16 2018

@author: root
"""
import serial
import time

portObjektiv = serial.Serial("/dev/ttyACM0",115200)
portObjektiv.write("softreset\n")
time.sleep(0.2)
portObjektiv.write("setposition 21000\n")
