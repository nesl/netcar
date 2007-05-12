#!/usr/bin/python

import sys
import GPSmodule
import SlogModule
import LOGmodule
import time
import os
import Queue


if(__name__ == "__main__"):
    #os.popen("sossrv -s /dev/ttyS0&")
    os.popen("pppd call gprs&")
    time.sleep(10)
    GPS = GPSmodule
    LOG = LOGmodule 
    SLOG = SlogModule.DataSlog()
    LOG.LOGmodule()
    GPS.GPSmodule()
    time.sleep(5)
    while True:
	try:
		(Tag,XML) = GPS.GPSXMLqueue.get(True,1)
		SLOG.ChangeDB(Tag[0],Tag[1],Tag[2],Tag[3])
		SLOG.ChangeXML(XML)
		Result = SLOG.Slog()
	except: 
		print "haha miss it"
		Result = "haha GPS has some problem"

	if "ConnectionFails" in Result:
		try:
			GPS.GPSXMLqueue.put((Tag,XML),True,0.5)
		except:
			print "missing again"
	else:
		pass

        try:
		(Tag,XML) = LOG.LOGXMLqueue.get(True,1)
		SLOG.ChangeDB(Tag[0],Tag[1],Tag[2],Tag[3])
		SLOG.ChangeXML(XML)
		Result = SLOG.Slog()
	except:
		print "No Log file"
		Result = "haha LOG missing"

	if "ConnectionFails" in Result:
		try:
			LOG.LOGXMLqueue.put((Tag,XML),True,0.5)
		except:
			print "Whoops"
	else:
		pass


