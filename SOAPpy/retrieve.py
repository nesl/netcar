from SOAPpy import WSDL
WSDLFILE = 'sensorbase2.wsdl'

server = WSDL.Proxy(WSDLFILE)



email = 'kimyh@ucla.edu'
password = 'password'
project_id = '85'
table_name = 'GPS'
#Available fields : Altitude,Latitude,Longitude,Precision,SatelliteCount,SID,Speed,TimeStamp,UID 
fields = 'Altitude,Latitude,Precision,SID'
tables = "p_%s_%s"%(project_id,table_name)
#condition = 1
condition = "Altitude > 100"
data_from = 0
data_to = 10000
re_type = 'csv'


csv = server.getData(email,password,fields,tables,condition,data_from,data_to,re_type)
print csv


email = 'kimyh@ucla.edu'
password = 'password'
project_id = '85'
table_name = 'GPRS'
#Available fields : Altitude,Latitude,Longitude,Precision,Speed,TimeStamp,Bing,Ping,UID 
fields = 'UID,Bing,Ping'
tables = "p_%s_%s"%(project_id,table_name)
condition = 1
#condition = "Altitude > 100"
data_from = 0
data_to = 10000
re_type = 'csv'

csv = server.getData(email,password,fields,tables,condition,data_from,data_to,re_type)
print csv
