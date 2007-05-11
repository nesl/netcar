import logging
import threading
import time
from DTN import queue
from DTN import message

class BaseModule(threading.Thread):
    """
        This is the base module. Every module should be derived from it and rewrite
        the functions for getMessageType(), getQueue()], and getReceiveFunction(). 
        GetQueue() will be used to register the queue with the DTN*Manager, and 
        receiveMessage() will be called if there is a message for that module.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self._log = logging.getLogger("BaseModule")
        self._log.setLevel(logging.DEBUG)
        self._queue = queue.FIFOQueue()

    def getMessageType(self):
        """ Return the message type which should be handled by this module. """
        return message.BASE_MESSAGE

    def getQueue(self):
        """ Return the queue for this module. """
        return self._queue

    def getReceiveFunction(self):
        """ Return the function that should be called if we receive a message. """
        return self.receiveMessage

    def receiveMessage(self, msg):
        """ This method will be called if the DTN manager received a message for
            that module.
        """
        self._log.debug("Received message: %s"%(msg,))

    def run(self):
        """ This is the main thread method. """
        counter = 1
        while 1:
            time.sleep(5)
            self._log.debug("adding message to queue")
            msg = message.Message(self.getMessageType(), "Base Message %d"%(counter,))
            counter += 1
            self._queue.addMessage(msg)

