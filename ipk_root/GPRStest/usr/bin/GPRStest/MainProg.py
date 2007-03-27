#!/usr/bin/python

import sys
import GPRSmodule
import SlogModule
import time
import os


if(__name__ == "__main__"):
    #os.popen("sossrv -s /dev/ttyS0&")
    #os.popen("pppd call gprs&")
    #time.sleep(10)
    GPRS = GPRSmodule
    SLOG = SlogModule.DataSlog()
    GPRS.GPRSmodule()
    time.sleep(5)
    while True:
        SLOG.ChangeDB('kimyh@ucla.edu','password','85','GPRS')
	try:
		XML = GPRS.GPRSXMLqueue.get(True,1)
		SLOG.ChangeXML(XML)
		Result = SLOG.Slog()
	except: 
		print "haha miss it"
		Result = "haha GPS has some problem"

	if "ConnectionFails" in Result:
		try:
			GPS.GPSXMLqueue.put(XML,True,0.5)
		except:
			print "missing again"
	else:
		pass




