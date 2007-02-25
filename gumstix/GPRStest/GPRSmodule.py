import sys
import gps
import time
import os
import Queue
import thread
import math

## Each Module has a Queue in it.
GPRSXMLqueue = Queue.Queue(20)

# Read Bluetooth MAC ID
#netcarID = os.popen("/usr/bin/hcitool dev")
#netcarID = netcarID.read()
#netcarID = netcarID.split()
#netcarID = netcarID[2]

# Bluetooth is not available
netcarID = "Test1"

class GPRSmodule:
    def __init__(self):
        self.tableOPEN = "<table>\n"
        self.tableCLOSE = "</table>\n"
        self.rowOPEN = "\t<row>\n"
        self.rowCLOSE = "\t</row>\n"
        self.fieldOPEN = "\t\t<field name=\""
        self.fieldOPEN2 = "\">"
        self.fieldCLOSE = "</field>\n"
        self.PREVIOUS = None
        try:
            thread.start_new_thread(self.runGPS, ())
        except thread.error:
            print error


    def MakeXML(self, Altitude, Latitude, Longitude, Precision, Speed, TimeStamp, UID, Bing, Ping):
	self.XML = self.tableOPEN
        self.XML = self.XML + self.rowOPEN
        self.XML = self.XML + self.fieldOPEN + "Altitude" + self.fieldOPEN2 + "%f"%Altitude + self.fieldCLOSE 
        self.XML = self.XML + self.fieldOPEN + "Latitude" + self.fieldOPEN2 + "%f"%Latitude + self.fieldCLOSE 
        self.XML = self.XML + self.fieldOPEN + "Longitude" + self.fieldOPEN2 + "%f"%Longitude + self.fieldCLOSE 
        self.XML = self.XML + self.fieldOPEN + "Precision" + self.fieldOPEN2 + "%f"%Precision + self.fieldCLOSE 
        self.XML = self.XML + self.fieldOPEN + "Speed" + self.fieldOPEN2 + "%s"%Speed + self.fieldCLOSE 

        self.TimeConvert = TimeStamp
        #print self.TimeConvert
        self.DZ = self.TimeConvert.split()
        #print self.DZ
        self.DY = self.DZ[0].split('/')
        self.DY = self.DY[2]+'-'+self.DY[1]+'-'+self.DY[0]
        self.TimeConvert = self.DY+' '+self.DZ[1]
        self.XML = self.XML + self.fieldOPEN + "TimeStamp" + self.fieldOPEN2 + "%s"%self.TimeConvert + self.fieldCLOSE   ## DD/MM/YYYY HH:MM:SS(GPS) -> YYYY-MM-DD HH:MM:SS(sensorbase)
        self.XML = self.XML + self.fieldOPEN + "UID" + self.fieldOPEN2 + "%s"%UID + self.fieldCLOSE 
        self.XML = self.XML + self.fieldOPEN + "Bing" + self.fieldOPEN2 + "%s"%Bing + self.fieldCLOSE 
        self.XML = self.XML + self.fieldOPEN + "Ping" + self.fieldOPEN2 + "%s"%Ping + self.fieldCLOSE 
        self.XML = self.XML + self.rowCLOSE + self.tableCLOSE
        #print self.XML
        return self.XML

    def runGPS(self):
        GPS = gps.GpsThread()
        GPS.start()
        time.sleep(5) ## wait until GPS settles
        while 1:
            st = time.time()
            try:
                bing=os.popen("/bin/bing -c 2 -e 2 192.168.1.3 ericsson.com")
                ping=os.popen("/bin/ping -c 2 ericsson.com")
            except:
                pass
            (lat,lon,alt) = GPS.getCoordinates()
       	    XML = self.MakeXML(alt,lat,lon,GPS.getPDOP(), GPS.getSpeed(), GPS.getTime(), netcarID, bing.read(), ping.read())
            GPRSXMLqueue.put(XML,True,0.5)
            ed = time.time() - st
            time.sleep(20-ed)

## Assumption : There is only one type

if(__name__ == "__main__"):
    Dummy = GPRSmodule()
    time.sleep(5)
    while True:
        try:
		print GPRSXMLqueue.get(True,3)
	except:
		print "HAHA"
		pass
        time.sleep(0.1)
    
