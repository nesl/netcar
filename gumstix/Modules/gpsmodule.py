import logging
import threading

from DTN import queue
from DTN import message

class LocationLoggingModule(BaseModule):
    """
        This module send the current location to the server
        whenever it notices that we moved for more than delta
    """
    def __init__(self, gps, delta=0):
        """
            gps: this is an instance to the gps thread object so we can
                 register ourselfs as interested in gps fix information.
        """
        BaseModule.__init__(self)
        self._log.setLevel(logging.DEBUG)
        self._queue = queue.FIFOQueue()

        self._delta = delta
        # register our gps fix function with the gps thread
        gps.registerGPSFixNotificationFunction(self.newGPSFix)

    def getMessageType(self):
        return message.LOCATION_LOGGING_MESSAGE

    def newGPSFix(self, gps):
        self._log.debug("new gps fix: lon %f lat %f alt %f"%gps.getCoordinates())
        msg = message.Message(self.getMessageType(), "%f,%f,%f"%gps.getCoordinates())
        self._queue.addMessage(msg)

    def run(self):
        """ For now, this thread doesn't do anything periodically. """
        pass
