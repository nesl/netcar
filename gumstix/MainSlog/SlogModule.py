import thread
import sys,os
import urllib
import urllib2

ERROR = "An error occurred while slogging."
SUCCESS = "Data successfully slogged!"

class DataSlog:
    def __init__(self):
        import urllib
        import urllib2
        self.sb_email = 'kimyh@ucla.edu'
        self.sb_password = 'password'
        self.sb_project_id = '73'
        self.sb_table = 'MoteGPS'
        try:
            pass
        except:
            print "Cannot Open File"

    def Slog(self):
        
        self.sb_api = 'http://sensorbase.org/alpha/upload.php' # the interface of sensorbase used for uploading data
        self.param = {'email' : self.sb_email,
                      'pw' : self.sb_password,
                      'project_id' : self.sb_project_id,
                      'data_string': self.xml,
                      'type':'xml',
                      'tableName': self.sb_table}
        self.data = urllib.urlencode(self.param)
        self.req = urllib2.Request(self.sb_api, self.data)
        self.response = urllib2.urlopen(self.req)
        self.SlogResult = "DATA POST result: " + self.response.read()
        self.response.close()
        return self.SlogResult

    def Burst(self):
        self.List = os.listdir(os.getcwd())
        for item in self.List:
            if 'xml' in item:
                try:
                    self.f = open(item)
                    self.xml = self.f.read()
                    self.f.close()
                    DD = self.Slog()
                    print DD
                except:
                    print "Error"
        

if(__name__ == "__main__"):
    A = DataSlog()
    A.Burst()
