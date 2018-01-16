# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 17:44:56 2018

@author: root
"""


import sys
import time
from socket import socket, AF_INET, SOCK_DGRAM

SERVER_IP   = '139.30.92.69'
PORT_NUMBER = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket( AF_INET, SOCK_DGRAM )
refMessage = "ref"

moveMessage = "mov_rel 100"

mySocket.sendto(refMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
time.sleep(1)

for cnt in range(1,10):
	mySocket.sendto(moveMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
	time.sleep(5)

sys.exit()