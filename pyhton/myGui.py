from Tkinter import *
import tkMessageBox
import iselControl as isel
import time

class CNCControl:
	
	def __init__(self, master):
		frame = Frame(master)
		frame.pack()
		
		self.canvasItems = []
		self.func = None
		self.IselController = None
		
		#everything to the right of the sidebar
		self.mainFrame = Frame(frame)
		
		#create controls frame
		self.controlFrame = Frame(self.mainFrame, width=600)
		
		#quit Button
		self.btnQuit = Button(self.controlFrame, text="Exit", command=frame.quit)
		self.btnQuit.grid(row=0, column=0)

		#pack control Frame
		self.controlFrame.grid(row = 1, column = 0)
		
		#pack main frame
		self.mainFrame.grid(row = 0, column = 0)
		
		#sidebar frame
		self.sideBarFrame = Frame(frame)
		
		#port selector
		self.entryPort = Entry(self.sideBarFrame)
		
		#equipement status labels
		#variables that can be updated to change the labels
		self.statusMessages = {
			"Isel" : StringVar(None,"Isel: Disconnected")
			}
		
		self.lblIsel = Label(self.sideBarFrame, textvariable=self.statusMessages["Isel"])
		
		# xyz move
		self.entryX = Entry(self.sideBarFrame)
		self.entryY = Entry(self.sideBarFrame)
		self.entryZ = Entry(self.sideBarFrame)
		self.btnMove = Button(self.sideBarFrame, text="Move to x,y,z", command=self.move_abs)
		
		#connect button for isel
		self.btnConnectIsel = Button(self.sideBarFrame, text="Connect to Isel", command=self.isel_connect)
		
		#init button for isel
		self.btnInitialize = Button(self.sideBarFrame, text="Initialize Isel", command=self.isel_initialize)
		
		self.entryPort.grid(row=0)
		self.lblIsel.grid(row=1)
		self.btnInitialize.grid(row=2)
		self.entryX.grid(row=3)
		self.entryY.grid(row=4)
		self.entryZ.grid(row=5)
		self.btnMove.grid(row=6)
		self.btnConnectIsel.grid(row=7)
		
		self.sideBarFrame.grid(row = 0, column = 1)
		
		# initial port setup
		self.entryPort.insert(0, "/dev/ttyS0")
		
	def isel_connect(self):
		#todo make this a variable
		self.IselController = isel.ISELController(self.entryPort.get())
		
		if not (self.IselController.port):
			tkMessageBox.showinfo(message="Couldn't Find Isel Controller, Conect and Try Again")
			self.statusMessages["Isel"].set("Isel: Disconnected")
		else:
			self.statusMessages["Isel"].set("Isel: Connected")
			
	def move_abs(self):
		x = self.entryX.get()
		y = self.entryY.get()
		z = self.entryZ.get()
		
		if self.IselController:
			self.IselController.move_abs_quick([x, 5000], [y, 5000], [0, 5000, 0, 5000])
		else:
			tkMessageBox.showinfo(message="Isel not connected")
		
	def isel_initialize(self):
		if self.IselController:
			self.IselController.initialize()
		else:
			tkMessageBox.showinfo(message="Isel not connected")
		
if __name__ == "__main__":
	root = Tk()
	app = CNCControl(root)
	root.mainloop()
