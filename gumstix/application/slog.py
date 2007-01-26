""" upload xml string to a table in sensorbase.
project id: 31
table name: newtable1
field name: Field_Name1, Field_Name2
two rows are uploaded in this xml string."""

import urllib
import urllib2

sb_email = 'kimyh@ucla.edu'
sb_password = 'password'
sb_project_id = '73'
sb_table = 'MoteGPS'
f = open('ddd.xml')
xml = f.readline()
f.close()

print xml
sb_api = 'http://sensorbase.org/alpha/upload.php' # the interface of sensorbase used for uploading data
param = {'email' : sb_email,
         'pw' : sb_password,
         'project_id' : sb_project_id,
         'data_string':xml,
         'type':'xml',
         'tableName':sb_table}

data = urllib.urlencode(param)
req = urllib2.Request(sb_api, data)
response = urllib2.urlopen(req)
print "DATA POST result: " + response.read()
response.close()
