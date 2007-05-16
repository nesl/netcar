import logging
import threading
import module
import math
import time
import sys, traceback
import urllib, urllib2

from DTN import queue
from DTN import message

longitude1degree = 111133.3333
latitude1degree = 222266.6667

class LocationLoggingModule(module.BaseModule):
    """
        This module send the current location to the server
        whenever it notices that we moved for more than delta
    """
    def __init__(self, gps, delta=0.0):
        """
            gps: this is an instance to the gps thread object so we can
                 register ourselfs as interested in gps fix information.
        """
        module.BaseModule.__init__(self)
        self._log.setLevel(logging.DEBUG)
        self._queue = queue.FIFOQueue()
        self._lastCoordinates = (0.0, 0.0, 0.0)

        self._delta = delta
        # register our gps fix function with the gps thread
        gps.registerGPSFixNotificationFunction(self.newGPSFix)

    def getMessageType(self):
        return message.GPS_MESSAGE

    def newGPSFix(self, gps):
        coordinates = gps.getCoordinates()
        diff = math.pow((self._lastCoordinates[0] - coordinates[0])*longitude1degree, 2) + math.pow((self._lastCoordinates[1] - coordinates[1]) * latitude1degree, 2)
        self._log.debug("new gps fix: lon %f lat %f alt %f diff from last: %fm "%(coordinates[0], coordinates[1], coordinates[2], diff))
        if diff >= self._delta * self._delta:
            self._lastCoordinates = coordinates
            msg = message.GPSMessage(lon = coordinates[0], 
                        lat = coordinates[1],
                        alt = coordinates[2],
                        precision = gps.getPDOP(),
                        satellites = gps.getSatellites(),
                        speed = gps.getSpeed(),
                        time = gps.getTime())
            self._queue.addMessage(msg)

    def run(self):
        """ For now, this thread doesn't do anything periodically. """
        pass

class LocationDecodingModule(module.BaseModule):
    """
        This module decodes gps messages on the receiving side.
    """
    def __init__(self):
        module.BaseModule.__init__(self)
        self._email = 'kimyh@ucla.edu'
        self._password = 'password'
        self._project = 85
        self._table = 'GPS'
        self._XMLForm = """
<table>
  <row>
    <field name="Altitude">%f</field>
    <field name="Latitude">%f</field>
    <field name="Longitude">%f</field>
    <field name="Precision">%f</field>
    <field name="SatelliteCount">%f</field>
    <field name="Speed">%f</field>
    <field name="TimeStamp">%s</field>
    <field name="UID">%s</field>
    <field name="SID">%s</field>
  </row>
</table>
"""
        self._sb_api = 'http://sensorbase.org/alpha/upload.php' # the interface of sensorbase used for uploading data

    def getMessageType(self):
        return message.GPS_MESSAGE

    def receiveMessage(self, msg):
        gpsMsg = message.GPSMessage(msg=msg)
        print gpsMsg, "received %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),) 

        xml = self._XMLForm%(gpsMsg.getAltitude(), 
                gpsMsg.getLatitude(),
                gpsMsg.getLongitude(),
                gpsMsg.getPrecision(),
                gpsMsg.getSatellites(),
                gpsMsg.getSpeed(),
                gpsMsg.getTime(),
                "Thomas",
                10)
        param = {'email': self._email,
            'pw' : self._password,
            'project_id' : self._project,
            'data_string' : xml,
            'type' : 'xml',
            'tableName' : self._table}
        try:
            data = urllib.urlencode(param)
            req = urllib2.Request(self._sb_api, data)
            response = urllib2.urlopen(req)
    
            print "SensorBase Result: "+response.read()
            response.close()
        except:
            e = sys.exc_info()[1]
            tr = sys.exc_info()[2]
            print "SensorBase: Something went wrong: " 
            print "%s\n%s"%(e, traceback.extract_tb(tr))
        
    def run(self):
        """ Nothing to do for now. """
        pass
