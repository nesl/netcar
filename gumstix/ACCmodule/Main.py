import BaseStation
import Queue
import SlogModule
import time
import os

class DataIntoXML:
    def __init__(self):
        self.tableOPEN = "<table>\n"
        self.tableCLOSE = "</table>\n"
        self.rowOPEN = "\t<row>\n"
        self.rowCLOSE = "\t</row>\n"
        self.fieldOPEN = "\t\t<field name=\""
        self.fieldOPEN2 = "\">"
        self.fieldCLOSE = "</field>\n"
        pass

    def ReadFormat(self):
        self.List = os.listdir(os.getcwd())
        for item in self.List:
            if '.form' in item:
                try:
                    self.f = open(item)
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
    
