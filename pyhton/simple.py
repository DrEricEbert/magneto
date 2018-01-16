import serial
import time

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
bytesToRead = port.in_waiting

sendCommand(port,"@01") #select x-Axis only
sendCommand(port,"@0d5000") #set reference speed
sendCommand(port,"@0R1") #home x-Axis
for i in xrange(1,10):
    sendCommand(port,"@0A "+mmMove(50)+",5000")#move axis 50mm steps with speed 5000
    time.sleep(1)
    
