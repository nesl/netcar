#!/usr/bin/python

import thread
import sys,os
import urllib
import urllib2
import time
import signal


#Logging setting
import logging
logger = logging.getLogger('SlogModule')
hdlr = logging.FileHandler('/home/SlogModule.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

#logger.warning('a warning message')
#logger.info('a log message')

ERROR = "An error occurred while slogging."
SUCCESS = "Data successfully slogged!"
IDNOTFOUND = "Hmm, you look lost. May I help you?" 
TABLENAMEERR = "supplied argument is not a valid MySQL result resource"
## handler
def GPRSbroken_handler(signum, frame):
     print 'GPRS connection broken, you need to re-establish it'
     logger.warning('GPRS connection broken, you need to re-establish it')

def Reconnect():
     os.popen("killall pppd")
     time.sleep(10)
     logger.info('Reconnect Start')
     if 'Invalid' in os.popen("pppd call gprs&").readline():
	os.popen("killall pppd")
	time.sleep(15)
	os.popen("pppd call gprs&")
     logger.info('pppd called')
     for i in range(30):
	#print "LOOPING"
        if 'ppp0' in os.popen('ifconfig').read():
           print "Re-established"
           logger.info('pppd re-established')
	   time.sleep(5)
           break
        time.sleep(0.5)
	if i==29:
	   os.popen("killall pppd")
	   time.sleep(5)
	   print "Fail to Re-establish"
           logger.info('fail to re-establish')
	   break


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
        try: 
		data = urllib.urlencode(param)
	        req = urllib2.Request(sb_api, data)
	        response = urllib2.urlopen(req)
	        SlogResult = "DATA POST result: " + response.read()
	        response.close()
		signal.alarm(0)
        except:
		logger.warning('Something is wrong with connection')
		print "Something is wrong with connection"
		signal.alarm(0)
		Reconnect()
		SlogResult = "DATA POST result: ConnectionFails Try Again"
	print SlogResult
        logger.info(SlogResult)
        return SlogResult


    def ChangeDB(self,sb_email,sb_password,sb_project_id,sb_table):
        self.sb_email = sb_email
        self.sb_password = sb_password
        self.sb_project_id = sb_project_id
        self.sb_table = sb_table
        #print self.sb_email
        #print self.sb_password
        #print self.sb_project_id
        #print self.sb_table

    def ChangeXML(self,XML):
	self.xml = XML


