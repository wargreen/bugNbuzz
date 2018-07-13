#!/usr/bin/env python2
#-*- coding: utf-8 -*-


import os
import sys
import os.path
import signal
import struct





def pstate_setter():
	
	if not os.path.exists('/dev/cpu_dma_latency'):
	        print "no PM QOS interface on this system!"
	        sys.exit(1)
	
	if len(sys.argv) == 1:
	        qos_target = 0
	elif len(sys.argv) == 2:
	        qos_target=int(sys.argv[1])
	else:
	        print "Syntax is: pm_qos [maximum latency in usecs] (default is 0)"
	        sys.exit(1)
	
	try:
	        fd = os.open('/dev/cpu_dma_latency', os.O_WRONLY)
	        os.write(fd, struct.pack("i",qos_target))
	        print "Writing", qos_target, "to /dev/cpu_dma_latency"
	        print "Press ^C to close /dev/cpu_dma_latency and exit"
	        signal.pause()
	
	except KeyboardInterrupt:
	        print "closing /dev/cpu_dma_latency"
	        os.close(fd)
	        sys.exit(0)
	        

if __name__ == "__main__":
	pstate_setter()
