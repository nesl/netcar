#!/usr/bin/python

from SOAPpy import WSDL


#Retrieving here

WSDLFILE = 'sensorbase2.wsdl'
server = WSDL.Proxy(WSDLFILE)



email = 'kimyh@ucla.edu'
password = 'password'
project_id = '85'
table_name = 'GPS'
#Available fields : Altitude,Latitude,Longitude,Precision,SatelliteCount,SID,Speed,TimeStamp,UID
fields = 'Altitude,Latitude,Longitude,Speed,Precision,TimeStamp,UID'
tables = "p_%s_%s"%(project_id,table_name)
condition = 1
#condition = "Altitude > 100"
data_from = 0
data_to = 10000
re_type = 'csv'


csv = server.getData(email,password,fields,tables,condition,data_from,data_to,re_type)




def hl():
    print "=" * 80


hl()


f = open('NetCar.kml','w')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<kml xmlns="http://earth.google.com/kml/2.0">\n')
f.write('<Folder>\n')
f.write('<name>NetCar GPS</name>\n')
f.write('<visibility>1</visibility>\n')

csv = csv.split('\n')

for line in csv:
    try:

	    line=line.split(',')
	    Altitude = line[0]
	    Longitude = line[2]
	    Latitude = line[1]
	    Speed = line[3]
	    Precision = line[4]
	    TimeStamp = line[5]
	    UID = line[6]
    


	    f.write('\t\t<Placemark>\n')
	    f.write('\t\t\t<name>%s</name>\n' % UID)
	    f.write('\t\t\t<description>Time: %s<br /> Altitude: %s m<br /> Speed: %s</description>\n' %(TimeStamp,Altitude,Speed))
	    f.write('\t\t\t<View>\n')
	    f.write('\t\t\t\t<longitude>%s</longitude>\n' % Longitude)
	    f.write('\t\t\t\t<latitude>%s</latitude>\n' % Latitude)
	    f.write('\t\t\t</View>\n')
	    f.write('\t\t\t<visibility>1</visibility>\n')
	    #f.write('\t\t\t<styleUrl>root://styleMaps#default?iconId=0x307</styleUrl>\n')
	    f.write('\t\t\t<Point><coordinates>%s,%s,45</coordinates></Point>\n' % (Longitude,Latitude) )
	    f.write('\t\t</Placemark>\n')

    except:
	    pass
    
f.write('</Folder>\n')
f.write('</kml>')
hl()    

