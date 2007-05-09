import sys
import time
import os
import Queue
import thread
import math

## Each Module has a Queue in it.
LOGXMLqueue = Queue.Queue(20)

# Read Bluetooth MAC ID
#netcarID = os.popen("/usr/bin/hcitool dev")
#netcarID = netcarID.read()
#netcarID = netcarID.split()
#netcarID = netcarID[2]

# Bluetooth is not available
dummy = open("/etc/netcarinit/netcarID")
netcarID = dummy.read()
dummy.close()
#netcarID = "Test1"

class LOGmodule:
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
            thread.start_new_thread(self.runLOG, ())
        except thread.error:
            print error


    def MakeXML(self, UID, LOG):
	self.XML = self.tableOPEN
        self.XML = self.XML + self.rowOPEN
        self.XML = self.XML + self.fieldOPEN + "UID" + self.fieldOPEN2 + "%s"%UID + self.fieldCLOSE 
        self.XML = self.XML + self.fieldOPEN + "LOG" + self.fieldOPEN2 + "%s"%LOG + self.fieldCLOSE 
        self.XML = self.XML + self.rowCLOSE + self.tableCLOSE
        #print self.XML
        return self.XML


    def runLOG(self):
        while 1:
            st = time.time()
       	    log = open("/home/SlogModule.log")
            data = log.read()
	    log.close()
	    log = open("/home/SlogModule.log",'w')
	    log.flush()
	    log.close()
	    XML = self.MakeXML(netcarID,data)
            LOGXMLqueue.put(XML,True,0.5)
            ed = time.time() - st
            time.sleep(30-ed)

    
