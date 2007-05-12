import logging
import threading
import module
import math

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

    def getMessageType(self):
        return message.GPS_MESSAGE

    def receiveMessage(self, msg):
        gpsMsg = message.GPSMessage(msg=msg)
        print gpsMsg

    def run(self):
        """ Nothing to do for now. """
        pass
