#!/usr/bin/python

from SOAPpy import WSDL
import csv

#Retrieving here

WSDLFILE = 'sensorbase2.wsdl'
server = WSDL.Proxy(WSDLFILE)



email = 'kimyh@ucla.edu'
password = 'password'
project_id = '85'
table_name = 'GPRS'
#UID,Altitude,Latitude,Longitude,Speed,Precision,TimeStamp,Ping,Bing
fields = 'Altitude,Latitude,Longitude,Speed,Precision,TimeStamp,UID'
tables = "p_%s_%s"%(project_id,table_name)
condition = 1
#condition = "Altitude > 100"
data_from = 0
data_to = 10000
re_type = 'csv'


data = server.getData(email,password,fields,tables,condition,data_from,data_to,re_type)

#print csv


def hl():
    print "=" * 80


hl()

db = open('GPRSbing.csv','w')
#db.write('Altitude,Latitude,Longitude,Speed,Precision,TimeStamp,UID,Bing\n')
db.write(data)
db.close()

    
f = open('GPRSbing.kml','w')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<kml xmlns="http://earth.google.com/kml/2.0">\n')
f.write('<Folder>\n')
f.write('<name>NetCar GPRSping</name>\n')
f.write('<visibility>1</visibility>\n')

data = csv.reader(open('GPRSbing.csv'))

for Altitude,Latitude,Longitude,Speed,Precision,TimeStamp,UID in data:
    print Altitude
#    break
##    
##for Altitude, Latitude, Longitude, Speed,Precision,TimeStamp,UID,Bing in data:
##
##    try:
##	    f.write('\t\t<Placemark>\n')
##	    f.write('\t\t\t<name>%s</name>\n' % UID)
##	    f.write('\t\t\t<description>Time: %s<br /> Altitude: %s m<br /> Speed: %s <br /> %s </description>\n' %(TimeStamp,Altitude,Speed,Bing))
##	    f.write('\t\t\t<View>\n')
##	    f.write('\t\t\t\t<longitude>%s</longitude>\n' % Longitude)
##	    f.write('\t\t\t\t<latitude>%s</latitude>\n' % Latitude)
##	    f.write('\t\t\t</View>\n')
##	    f.write('\t\t\t<visibility>1</visibility>\n')
##	    #f.write('\t\t\t<styleUrl>root://styleMaps#default?iconId=0x307</styleUrl>\n')
##	    f.write('\t\t\t<Point><coordinates>%s,%s,45</coordinates></Point>\n' % (Longitude,Latitude) )
##	    f.write('\t\t</Placemark>\n')
##
##    except:
##	    pass
    
f.write('</Folder>\n')
f.write('</kml>')
hl()    

