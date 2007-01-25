#!/usr/bin/python

import thread
import sys,os
import urllib
import urllib2

ERROR = "An error occurred while slogging."
SUCCESS = "Data successfully slogged!"
IDNOTFOUNDERR = "Hmm, you look lost. May I help you?" 
TABLENAMEERR = "supplied argument is not a valid MySQL result resource"

def Slog(sb_email,sb_password,sb_project_id,sb_table,xml):
	sb_api = 'http://sensorbase.org/alpha/upload.php' 
	param = {'email' : sb_email,
	         'pw' : sb_password,
	         'project_id' : sb_project_id,
	         'data_string': xml,
	         'type':'xml',
	         'tableName': sb_table}
	print param
	data = urllib.urlencode(param)
	req = urllib2.Request(sb_api, data)
	response = urllib2.urlopen(req)
	SlogResult = "DATA POST result: " + response.read()
	response.close()
	print SlogResult
        return SlogResult

def Burst():
	List = os.listdir(os.getcwd())
        for item in List:
            if 'xml' in item:
                try:
                    f = open(item)
                    xml = f.read()
		    print xml
                    f.close()
                    DD = Slog()
                    print DD
                except:
                    print "Error"


def ChangeDBfromFile(filename):
	if '.table' in filename:
		try:
			f = open(filename)
			TOC = f.read()
			f.close()
                except:
			print "No format or something"
        TOC = TOC.split('\n')

        for item in TOC:
            if 'email =' in item:
                temp = item.split(' = ')
                sb_email = temp[1]
            elif 'password =' in item:
                temp = item.split(' = ')
                sb_password = temp[1]
            elif 'project_id =' in item:
                temp = item.split(' = ')
                sb_project_id = temp[1]
            elif 'table =' in item:
                temp = item.split(' = ')
                sb_table = temp[1]
            else:
                pass
            
	return (sb_email,sb_password,sb_project_id,sb_table)        

if(__name__ == "__main__"):
	dummysb_email = 'kimyh@ucla.edu'
	dummysb_password = 'password\r'
	dummysb_project_id = '73'
	dummysb_table = 'MoteGPS'
	dummyxml = open('data.xml')
	dummyxml = dummyxml.read()
	Slog(dummysb_email,dummysb_password,dummysb_project_id,dummysb_table,dummyxml)

