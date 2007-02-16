#!/usr/bin/python

import sys
import GPSmodule
import SlogModule
import time
import os


if(__name__ == "__main__"):
    #os.popen("sossrv -s /dev/ttyS0&")
    os.popen("pppd call gprs&")
    time.sleep(10)
    GPS = GPSmodule
    SLOG = SlogModule.DataSlog()
    GPS.GPSmodule()
    time.sleep(5)
    while True:
        SLOG.ChangeDB('kimyh@ucla.edu','password','85','GPS')
	XML = GPS.GPSXMLqueue.get()
	SLOG.ChangeXML(XML)
	Result = SLOG.Slog()
	if "ConnectionFails" in Result:
		try:
			GPS.GPSXMLqueue.put(XML,True,0.5)
		except:
			print "missing again"
	else:
		pass




