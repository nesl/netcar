import gps
import time
import os

class LogIntoXML:
    def __init__(self):
        self.tableOPEN = "<table>\n"
        self.tableCLOSE = "</table>\n"
        self.rowOPEN = "\t<row>\n"
        self.rowCLOSE = "\t</row>\n"
        self.fieldOPEN = "\t\t<field name=\""
        self.fieldOPEN2 = "\">\n"
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
                temp = temp.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f" + self.fieldClose % Altitude
            elif 'Latitude' in item:
                temp = temp.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f" + self.fieldClose % Latitude
            elif 'Longitude' in item:
                temp = temp.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f" + self.fieldClose % Longitude
            elif 'Precision' in item:
                temp = temp.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f" + self.fieldClose % Precision
            elif 'SatelliteCount' in item:
                temp = temp.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f" + self.fieldClose % SatelliteCount
            elif 'Speed' in item:
                temp = temp.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%s" + self.fieldClose % Speed
            elif 'TimeStamp' in item:
                temp = temp.split(" : ")
                self.TimeConvert = TimeStamp
                DZ = self.TimeConvert.split
                DY = DZ[0].split('/')
                DY = DY[2]+'-'+DY[1]+'-'+DY[0]
                self.TimeConvert = DY+DZ[1]
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%s" + self.fieldClose % self.TimeConvert  ## DD/MM/YYYY HH:MM:SS(GPS) -> YYYY-MM-DD HH:MM:SS(sensorbase)
            elif 'UID' in item:
                temp = temp.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f" + self.fieldClose % UID
            elif 'SID' in item:
                temp = temp.split(" : ")
                self.XML = self.XML + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f" + self.fieldClose % SID
        self.XML = self.XML + self.rowCLOSE + self.fieldCLOSE
        print self.XML

## Assumption : There is only one type

if(__name__ == "__main__"):
    GPS = gps.GpsThread()
    GPS.start()
    B = LogIntoXML()
    B.ReadFormat()

    while 1:
        (lat,lon,alt) = GPS.getCoordinates()
        B.MakeXML(alt,lat,lon,GPS.getSatelliteStatistics(), GPS.getSatellites(), GPS.getSpeed(), GPS.getTime(), 10, 10)
        time.sleep(5)
    
