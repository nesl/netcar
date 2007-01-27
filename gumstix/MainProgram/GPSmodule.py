import gps
import time
import os
import Queue
import thread

## Each Module has a Queue in it.
GPSqueue = Queue.Queue(20)


class GPSmodule:
    def __init__(self):
        self.tableOPEN = "<table>\n"
        self.tableCLOSE = "</table>\n"
        self.rowOPEN = "\t<row>\n"
        self.rowCLOSE = "\t</row>\n"
        self.fieldOPEN = "\t\t<field name=\""
        self.fieldOPEN2 = "\">"
        self.fieldCLOSE = "</field>\n"
        try:
            thread.start_new_thread(self.runGPS, ())
        except thread.error:
            print error

    def ReadFormat(self):
        try:
            self.f = open('GPSDB.form')
            self.format = self.f.read()
            self.f.close()
        except:
            print "Error"
        self.format = self.format.split('\n')
        return self.format

    def MakeXML(self, Altitude, Latitude, Longitude, Precision, SatelliteCount, Speed, TimeStamp, UID, SID):
        self.XML = self.tableOPEN
        self.XML = self.XML + self.rowOPEN
        self.XMLstructure = self.ReadFormat()
        for item in self.XMLstructure:
            if 'Altitude' in item:
                temp = item.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f"%Altitude + self.fieldCLOSE 
            elif 'Latitude' in item:
                temp = item.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f"%Latitude + self.fieldCLOSE 
            elif 'Longitude' in item:
                temp = item.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f"%Longitude + self.fieldCLOSE 
            elif 'Precision' in item:
                temp = item.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f"%Precision + self.fieldCLOSE 
            elif 'SatelliteCount' in item:
                temp = item.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f"%SatelliteCount + self.fieldCLOSE 
            elif 'Speed' in item:
                temp = item.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%s"%Speed + self.fieldCLOSE 
            elif 'TimeStamp' in item:
                temp = item.split(" : ")
                self.TimeConvert = TimeStamp
		print self.TimeConvert
                self.DZ = self.TimeConvert.split()
		print self.DZ
                self.DY = self.DZ[0].split('/')
                self.DY = self.DY[2]+'-'+self.DY[1]+'-'+self.DY[0]
                self.TimeConvert = self.DY+' '+self.DZ[1]
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%s"%self.TimeConvert + self.fieldCLOSE   ## DD/MM/YYYY HH:MM:SS(GPS) -> YYYY-MM-DD HH:MM:SS(sensorbase)
            elif 'UID' in item:
                temp = item.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%d"%UID + self.fieldCLOSE 
            elif 'SID' in item:
                temp = item.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%d"%SID + self.fieldCLOSE 
        self.XML = self.XML + self.rowCLOSE + self.tableCLOSE
        print self.XML
        return self.XML

    def runGPS(self):
        GPS = gps.GpsThread()
        GPS.start()
        time.sleep(5) ## wait until GPS settles
        while 1:
            (lat,lon,alt) = GPS.getCoordinates()
            print GPS.getTime()
            XML = self.MakeXML(alt,lat,lon,10, GPS.getSatellites(), GPS.getSpeed(), GPS.getTime(), 10, 10)
	    print XML
            try:
                GPSqueue.put(XML,True,0.5)
            except:
                print "You're missing GPS data"
            time.sleep(1)

## Assumption : There is only one type

if(__name__ == "__main__"):
    Dummy = GPSmodule()
    time.sleep(5)
    while True:
        print GPSqueue.get()
        time.sleep(0.1)
    
