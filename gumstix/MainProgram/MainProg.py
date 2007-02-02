#!/usr/bin/python

import sys
sys.path.append("/home/MainProgram")
import GPSmodule
import Accel
import SlogModule
import time
import os


if(__name__ == "__main__"):
    #os.popen("sossrv -s /dev/ttyS0&")
    os.popen("pppd call gprs&")
    time.sleep(10)
    GPS = GPSmodule
    #ACC = Accel
    SLOG = SlogModule.DataSlog()
    GPS.GPSmodule()
    #ACC.AccXMLPut()
    time.sleep(5)
    while True:
        SLOG.ChangeDB('kimyh@ucla.edu','password','85','GPS')
        XML = GPS.GPSXMLqueue.get()
	SLOG.ChangeXML(XML)
        SLOG.Slog()
        #SLOG.ChangeDB('kimyh@ucla.edu','password','85','Accel')
	#XML =  ACC.AccXMLQueue.get()
        #SLOG.ChangeXML(XML)
        #SLOG.Slog()
        
        
