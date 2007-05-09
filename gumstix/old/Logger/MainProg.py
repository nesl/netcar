#!/usr/bin/python

import sys
import LOGmodule
import SlogModule
import time
import os


if(__name__ == "__main__"):
    #os.popen("sossrv -s /dev/ttyS0&")
    #os.popen("pppd call gprs&")
    #time.sleep(10)
    LOG = LOGmodule
    SLOG = SlogModule.DataSlog()
    LOG.LOGmodule()
    time.sleep(5)
    while True:
        SLOG.ChangeDB('kimyh@ucla.edu','password','85','Debug')
	try:
		XML = LOG.LOGXMLqueue.get(True,1)
		SLOG.ChangeXML(XML)
		Result = SLOG.Slog()
	except: 
		print "haha miss it"
		Result = "haha LOG has some problem"

	if "ConnectionFails" in Result:
		try:
			LOG.LOGXMLqueue.put(XML,True,0.5)
		except:
			print "missing again"
	else:
		pass




