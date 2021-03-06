#!/usr/bin/python

import thread
import sys,os
import urllib
import urllib2
import signal

ERROR = "An error occurred while slogging."
SUCCESS = "Data successfully slogged!"
IDNOTFOUND = "Hmm, you look lost. May I help you?" 
TABLENAMEERR = "supplied argument is not a valid MySQL result resource"
## handler
def GPRSbroken_handler(signum, frame):
     print 'GPRS connection broken, you need to re-establish it'
     raise IOError, "Couldn't slog it"



## Assume there is only one DB format and table definition file.
## Later on, it'll be changed to match appropriate Data file and format file.

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
        ##print "babao"+self.table
        return self.format

    def MakeXML(self):
        self.XMLstructure = self.ReadFormat()
        for item in self.XMLstructure:
            print item
        print self.XMLstructure
    def ChangeXML(self,XML):
	self.XML = XML

## Assumption : There is only one type

class DataSlog:
    def __init__(self):
        self.sb_email = 'kimyh@ucla.edu'
        self.sb_password = 'password'
        self.sb_project_id = '73'
        self.sb_table = 'MoteGPS'
	self.xml = ''
        try:
            pass
        except:
            print "Cannot Open File"

    def Slog(self):
        
        sb_api = 'http://sensorbase.org/alpha/upload.php' # the interface of sensorbase used for uploading data
        param = {'email' : self.sb_email,
                      'pw' : self.sb_password,
                      'project_id' : self.sb_project_id,
                      'data_string': self.xml,
                      'type':'xml',
                      'tableName': self.sb_table}
	print param
	signal.signal(signal.SIGALRM, GPRSbroken_handler)
	signal.alarm(15)
        data = urllib.urlencode(param)
        req = urllib2.Request(sb_api, data)
        response = urllib2.urlopen(req)
        SlogResult = "DATA POST result: " + response.read()
        response.close()
	print SlogResult
	signal.alarm(0)
        return SlogResult

    def Burst(self):
        List = os.listdir(os.getcwd())
        for item in List:
            if 'xml' in item:
                try:
                    f = open(item)
                    self.xml = f.read()
		    print self.xml
                    f.close()
                    DD = self.Slog()
                    print DD
                except:
                    print "Error"

    def ChangeDB(self,sb_email,sb_password,sb_project_id,sb_table):
        self.sb_email = sb_email
        self.sb_password = sb_password
        self.sb_project_id = sb_project_id
        self.sb_table = sb_table
        print self.sb_email
        print self.sb_password
        print self.sb_project_id
        print self.sb_table

    def ChangeXML(self,XML):
	self.xml = XML

    def ChangeDBfromFile(self):
        List = os.listdir(os.getcwd())
        for item in List:
            if '.table' in item:
                try:
                    f = open(item)
                    TOC = f.read()
                    f.close()

                except:
                    print "No format or something"
        TOC = TOC.split('\n')

        for item in TOC:
	    ## This strip removes carriage return
	    item = item.strip()
            if 'email =' in item:
                temp = item.split(' = ')
                self.sb_email = temp[1]
            elif 'password =' in item:
                temp = item.split(' = ')
                self.sb_password = temp[1]
            elif 'project_id =' in item:
                temp = item.split(' = ')
                self.sb_project_id = temp[1]
            elif 'table =' in item:
                temp = item.split(' = ')
                self.sb_table = temp[1]
            else:
                pass
            
        

if(__name__ == "__main__"):
    ##B = LogIntoXML()
    ##B.ReadFormat()
    ##B.MakeXML()
    A = DataSlog()
    A.ChangeDB('kimyh@ucla.edu','password','73','MoteGPS')
    A.ChangeDBfromFile()
    A.Burst()
    A.Slog()
