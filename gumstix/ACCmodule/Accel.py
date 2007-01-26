import BaseStation
import Queue
import time
import os
import Queue

class DataIntoXML:
    def __init__(self):
        self.tableOPEN = "<table>\n"
        self.tableCLOSE = "</table>\n"
        self.rowOPEN = "\t<row>\n"
        self.rowCLOSE = "\t</row>\n"
        self.fieldOPEN = "\t\t<field name=\""
        self.fieldOPEN2 = "\">"
        self.fieldCLOSE = "</field>\n"
	self.NoofBurst = 1
	self.Acc = BaseStation.BaseStation()
	time.sleep(1)


    def ReadFormat(self):
        List = os.listdir(os.getcwd())
        for item in List:
            if '.form' in item:
                try:
                    f = open(item)
                    format = f.read()
                    f.close()
                except:
                    print "Error"
        format = format.split('\n')
        return format

    def MakeXML(self):
	self.XML = self.tableOPEN
	index = 0
	AccX = self.Acc.d0
	AccY = self.Acc.d1
	AccZ = self.Acc.d0
	for item in AccX:
		Y = AccY[index]
		Z = AccZ[index]
		self.XML = self.XML + self.MakeROW(item[1],Y[1],Z[1],item[0],1,1)
	self.XML = self.XML + self.tableCLOSE
	print self.XML

    def MakeROW(self, AccelX, AccelY, AccelZ, TimeStamp, UID, SID):
        self.ROW = self.rowOPEN
        self.XMLstructure = self.ReadFormat()
        for item in self.XMLstructure:
            if 'AccelX' in item:
                temp = item.split(" : ")
                self.ROW = self.ROW + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f"%AccelX + self.fieldCLOSE 
            elif 'AccelY' in item:
                temp = item.split(" : ")
                self.ROW = self.ROW + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f"%AccelY + self.fieldCLOSE 
            elif 'AccelZ' in item:
                temp = item.split(" : ")
                self.ROW = self.ROW + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f"%AccelZ + self.fieldCLOSE 
            elif 'TimeStamp' in item:
                temp = item.split(" : ")
                self.ROW = self.ROW + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%f"%TimeStamp + self.fieldCLOSE 
            elif 'SatelliteCount' in item:
                temp = item.split(" : ")
            elif 'UID' in item:
                temp = item.split(" : ")
                self.ROW = self.ROW + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%d"%UID + self.fieldCLOSE 
            elif 'SID' in item:
                temp = item.split(" : ")
                self.ROW = self.ROW + self.fieldOPEN + temp[0] + self.fieldOPEN2 + "%d"%SID + self.fieldCLOSE 
        self.ROW = self.ROW + self.rowCLOSE
        print self.ROW
        return self.ROW
    
if(__name__ == "__main__"):
	import SlogModule
	SLOG = SlogModule.DataSlog()
	SLOG.ChangeDBfromFile()
	DataQ = Queue.Queue(10)
	A = DataIntoXML()
	A.ReadFormat()

	while 1:
		A.MakeXML()
		DataQ.put(A.XML,True,0.5)  # this is XML
	        SLOG.ChangeXML(DataQ.get())
	        SLOG.Slog()
	        time.sleep(1)
