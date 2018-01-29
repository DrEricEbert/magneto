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



def objectivePosition(position):
	objMessage = "obj_pos "+str(position)
	print("Position: "+str(position)+"\r\n");
	mySocket.sendto(objMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
	time.sleep(1)

def stageReference():
	refMessage = "ref"
	mySocket.sendto(refMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
	time.sleep(10)
	
def stagePosition(position):
	moveMessage = "mov_rel "+str(position)
	print("Position: "+str(position)+"\r\n");
	mySocket.sendto(objMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
	time.sleep(1)

#Check Objective position range
#for cnt in range(1,20):
#	position = 18000+1000*cnt
#	objectivePosition(position)

objectivePosition(25000)	


#mySocket.sendto(refMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
#time.sleep(10)
#Socket.sendto(moveMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))

#mySocket.sendto(objMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))

#for cnt in range(1,100):
#	position = 18000+cnt*300
#	objMessage = "obj_pos "+str(position)
#	print("Position: "+str(position)+"\r\n");
#	mySocket.sendto(objMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
#	#mySocket.sendto(moveMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
#	time.sleep(.3)

#mySocket.sendto(refMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))


sys.exit()