import BaseStation
import Queue
import time
import os
import Queue
import thread

## Accel->XML->put queue

AccXMLQueue = Queue.Queue(20)

class AccXMLPut:
    def __init__(self):
        self.tableOPEN = "<table>\n"
        self.tableCLOSE = "</table>\n"
        self.rowOPEN = "\t<row>\n"
        self.rowCLOSE = "\t</row>\n"
        self.fieldOPEN = "\t\t<field name=\""
        self.fieldOPEN2 = "\">"
        self.fieldCLOSE = "</field>\n"
	self.NoofBurst = 1
        try:
            thread.start_new_thread(self.RunAccXML, ())
        except thread.error:
            print error
            
    
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

    def MakeXML(self,AccX,AccY,AccZ):
	self.XML = self.tableOPEN
	index = 0
	for item in AccX:
		Y = AccY[index]
		Z = AccZ[index]
		self.XML = self.XML + self.MakeROW(item[1],Y[1],Z[1],item[0],1,1)
	self.XML = self.XML + self.tableCLOSE
	#print self.XML
	try:
            AccXMLQueue.put(self.XML,True,1)
        except:
            print "You are losing ACC XML DATA"

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
        #print self.ROW
        return self.ROW

    def RunAccXML(self):
        Acc = BaseStation
        Acc.BaseStation()
        while True:
            Temp = Acc.AccelQueue.get()
            self.MakeXML(Temp[0],Temp[1],Temp[0])
        
        
    
if(__name__ == "__main__"):
    DD = AccXMLPut()
    DD.RunAccXML()
    while True:
	print AccXMLQueue.get()

