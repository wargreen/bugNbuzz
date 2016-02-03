#!/usr/bin/env python2
# coding=utf8


from time import time, sleep
from liblo import *
import curses
import sys
import signal
try:
	import patcher
except ImportError:
    print('patcher import failed')


class MyServer(ServerThread):
	def __init__(self):
		ServerThread.__init__(self, 8000)
		print "Ready to receive (your order)"
		try:	
			self.target = Address("localhost",9951)
			self.bitwig = Address("localhost",8175)
		except liblo.AddressError as err:
			print(err)
			sys.exit()
		self.stdscr = curses.initscr()
		curses.cbreak()
		curses.noecho()
		self.stdscr.nodelay(True)
		self.stdscr.addstr(0,0,"******************************* SooperLooper ****************************",curses.A_REVERSE)
		self.stdscr.addstr(4,0,"All    ",curses.A_REVERSE)
		for l in range(4):
			self.stdscr.addstr(l+5,0,"loop "+str(l+1)+ " ",curses.A_REVERSE)
		self.stdscr.addstr(10,0,"q : quit / 1-4 : loop selection / a : all / r : RecPlayOver / u : UndoRedo / s : Stop and Clear / c : connect Bitwig to SL / m : put all bitwig track to monitor",curses.A_DIM)
		self.ping()
		self.states = [0.0,0.0,0.0,0.0,0.0]
		self.stdscr.addstr(13,0,"********************************** Jacket *******************************",curses.A_REVERSE)
		self.stdscr.addstr(14, 0, "Host :  osc.udp://xosc:9000")
		for l in range(5):
			self.stdscr.addstr(l+16,0,"button "+str(l+1)+ " ",curses.A_REVERSE)

#		self.stdscr.addstr(22,0,"record / play ",curses.A_REVERSE)
#		self.stdscr.addstr(23,0,"     undo     ",curses.A_REVERSE)
#		self.stdscr.addstr(24,0,"     stop     ",curses.A_REVERSE)
			
		for l in range(5):
			self.stdscr.addstr(l+16,20,"led "+str(l+1)+ " ",curses.A_REVERSE)
		for l in range(5):
			self.stdscr.addstr(l+16,32,"analog "+str(l+1)+ " ",curses.A_REVERSE)



	def quit(self):
		curses.nocbreak()
		curses.echo()
		curses.endwin()
		print("bye bye !!")
		sys.exit(0)

	@make_method('/pong', 'ssi')
	def pong_callback(self, path, args):
		h, v, l = args
		self.stdscr.addstr(1, 0, "Host : "+ h +" version : "+ v)
		self.stdscr.addstr(2, 0, str(l) +" loop(s) instancied")
		self.stdscr.refresh()
		if(l<4):
			send(self.target,"/loop_add",l+1,1.0) # Déjà fait dans la session
			send(self.target,"/ping","osc.udp://localhost:8000/","/pong")
		else:
			for l in range(4):
				send(self.target,"/sl/"+str(l)+"/register_auto_update","state",100,"osc.udp://localhost:8000/","/update")
		self.loopSelect(0)
		send(self.target,"/register_auto_update","tempo", 100, "osc.udp://localhost:8000/","/tempo")
	
	@make_method('/tempo', 'isf')
	def tempo(self, path, args):
		send(self.bitwig,"/tempo/raw", args[2])
		self.stdscr.addstr(4,20,"BPM : "+str(args[2]),curses.A_REVERSE)
	
	def getState(self,s):
		if s == 0.0:
			return "Off         "
		if s == 1.0:
			return "WaitStart   "
		if s == 2.0:
			return "Recording   "
		if s == 3.0:
			return "WaitStop    "
		if s == 4.0:
			return "Playing     "
		if s == 5.0:
			return "Overdubbing "
		if s == 6.0:
			return "Multiplying "
		if s == 7.0:
			return "Inserting   "
		if s == 8.0:
			return "Replacing   "
		if s == 9.0:
			return "Delay       "
		if s == 10.0:
			return "Muted       "
		if s == 11.0:
			return "Scratching  "
		if s == 12.0:
			return "OneShot     "
		if s == 13.0:
			return "Substitute  "
		if s == 14.0:
			return "Paused      "

	@make_method('/update', 'isf')
	def update(self, path, args):
		l, c, s = args
		self.states[l]=s
		self.stdscr.addstr(l+5,10,self.getState(s))

	@make_method('/battery','f')
	def battery(self, path, args):
		self.battery = args	

	@make_method('/inputs/digital','iiiiiiiiiiiiiiii')
	def buttons(self, path, args):
		if (self.buttons != args):
			self.buttons = args	
			if self.buttons[15]==0:
				self.loopRecPlay()
			if self.buttons[14]==0:
				self.loopStop()
			if self.buttons[13]==0:
				self.loopUndo()
	
	#	if buttons[12]==0:
	#		this.loopSelect(-1)
	#	if buttons[11]==0:
	#		this.loopSelect(3)
	#	if buttons[10]==0:
	#		this.loopSelect(2)
	#	if buttons[9]==0:
	#		this.loopSelect(1)
	#	if buttons[8]==0:
	#		this.loopSelect(0)
	


	@make_method('/inputs/analogue','ffffffffffffffff')
	def potar(self, path, args):
		potar = args

	
	@make_method(None, None)
	def fallback(self, path, args):
		print >> sys.stderr, "received message '"+str(path)+"' "+str(args)
	

########## Send methods ###########

	def ping(self):
		send(self.target,"/ping","osc.udp://localhost:8000/","/pong")
	
	def loopSelect(self,loopnum):
		self.loopnum=loopnum
		send(self.target,"/sl/set","selected_loop_num",int(self.loopnum))
		send(self.target,"/sl/-1/set","dry",0)
		send(self.target,"/sl/"+str(self.loopnum)+"/set","dry",1)
		for l in range(5):
			self.stdscr.addstr(l+4,8," ")	
		self.stdscr.addstr(self.loopnum+5,8,"*",curses.A_BOLD)

	def loopRecPlay(self):
		if self.states[self.loopnum]==0.0 or self.states[self.loopnum]==14.0:
			send(self.target,"/sl/"+str(self.loopnum)+"/hit","record")
		elif self.states[self.loopnum]==2.0:
			send(self.target,"/sl/"+str(self.loopnum)+"/hit","record")
		else:
			send(self.target,"/sl/"+str(self.loopnum)+"/hit","overdub")	

	def loopStop(self):
		send(self.target,"/sl/"+str(self.loopnum)+"/hit","pause")
		self.states[self.loopnum]=0.0

	def loopUndo(self):
		send(self.target,"/sl/"+str(self.loopnum)+"/hit","undo")

	def connect(self):
		patcher.connect_sl()

############ Bitwig config #############

	def bitwig_monitor(self):
		for bank in range(4):
			send(self.bitwig,"/track/bank/page/-")
		
		for bank in range(4):
			for track in range (7):
				track += 1
				send(self.bitwig,"/track/"+str(track)+"/monitor", 1)
			send(self.bitwig,"/track/bank/page/+")
	
############ Interactions #############	

	def interact(self):
		c = self.stdscr.getch()
		if c==ord('q'):
			self.quit()
		elif c==ord('a'):
			self.loopSelect(-1)
		elif c==ord('1'):
			self.loopSelect(0)
		elif c==ord('2'):
			self.loopSelect(1)
		elif c==ord('3'):
			self.loopSelect(2)
		elif c==ord('4'):
			self.loopSelect(3)
		elif c==ord('r'):
			self.loopRecPlay()
		elif c==ord('s'):
			self.loopStop()
		elif c==ord('u'):
			self.loopUndo()
		elif c==ord('c'):
			self.connect()
		elif c==ord('m'):
			self.bitwig_monitor()


try:
    server = MyServer()
except ServerError, err:
    print str(err)
    sys.exit()

server.start()

while True:
	server.interact()
	sleep(0.1)

server.quit()
