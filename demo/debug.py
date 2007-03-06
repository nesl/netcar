import sys
import os
from SOAPpy import WSDL
WSDLFILE = 'sensorbase2.wsdl'

server = WSDL.Proxy(WSDLFILE)

print sys.argv[1]

email = 'kimyh@ucla.edu'
password = 'password'
project_id = '85'
table_name = 'Debug'
fields = 'LOG'
tables = "p_%s_%s"%(project_id,table_name)
#condition = 1
condition = "UID=\"%s\""%sys.argv[1]
data_from = 0
data_to = 10000
re_type = 'csv'

csv = server.getData(email,password,fields,tables,condition,data_from,data_to,re_type)
dummy = open('%s.log'%sys.argv[1],'w')
dummy.flush()
dummy.write(csv)
dummy.close()

os.popen('%s.log'%sys.argv[1])
