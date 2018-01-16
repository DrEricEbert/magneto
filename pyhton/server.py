# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 17:44:25 2018

@author: root
"""


from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import serial
import time

PORT_NUMBER = 5000
SIZE = 1024

hostName = gethostbyname( '0.0.0.0' )

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

def sendCommand(port, command):
		if port:
			print "Sending %s..." % command,
			port.write(command+"\r")
			c = port.read()
			mess = {'0':"Okay",
					'1':"Error in numeric value",
					'2':"Limit switch triggered, run reference",
					'3':"Incorrect axis specification",
					'4':"No Axis defined",
					'5':"Syntax Error",
					'6':"End of CNC Memory",
					'7':"Incorrect Number of parameters",
					'8':"Command not allowed",
					'9':"System Error",
					'D':"Speed not permitted",
					'F':"User Stop",
					'G':"Invalid Data Field",
					'H':"Cover Open",
					'R':"Reference Error, run reference"
					}
			if (c in mess.keys()):
				print mess[c]
			else:
				print "Unknown Error Code (%s)" % c 
			
			return c
		else:
			return "P" #no port message (custom)
def mmMove(value_mm):
    steps = value_mm/0.00625
    return str(steps)

    
port = serial.Serial("/dev/ttyS0",19200)

#sendCommand(port,"@01") #select x-Axis only
#sendCommand(port,"@0d5000") #set reference speed
#sendCommand(port,"@0R1") #home x-Axis

print "Test server listening on port {0}\n".format(PORT_NUMBER)

while True:
    (data,addr) = mySocket.recvfrom(SIZE)
    print data
    mylist = data.split(" ")
    if mylist[0] == "ref":
        sendCommand(port,"@01") #select x-Axis only
        sendCommand(port,"@0d5000") #set reference speed
        sendCommand(port,"@0R1") #home x-Axis
    if mylist[0] == "mov_rel":
        sendCommand(port,"@0A "+mmMove(int(mylist[1]))+",5000")#move axis 50mm steps with speed 5000   
sys.exit()