import Queue as pyQueue
import message

class Queue:
    """ 
        This is the generic queue class. All the queues should inherit
        from this class in order to conform to the DTN requirements.
    """
   
    def __init__(self):
        pass

    def isEmpty(self):
        """ Returns True if the queue is empty, False otherwise. """
        return True

    def getNext(self):
        """ Returns the next message in the queue, but does not remove it
            from the queue!
        """
        return None

    def removeNext(self):
        """ Removes the next element from the queue. """
        return None

class FIFOQueue(Queue):
    """
        This is a simple example of a FIFO queue.
    """
    def __init__(self):
        Queue.__init__(self)
        #setup the logging system
        import logging
        self._log = logging.getLogger("FIFOQueue")
        self._log.setLevel(logging.DEBUG)

        self._queue = []
    
    def isEmpty(self):
        if len(self._queue) == 0:
            return True
        else:
            return False

    def getNext(self):
        if not self.isEmpty():
            return self._queue[0]
        else:
            return None

    def removeNext(self):
        if not self.isEmpty():
            if len(self._queue) == 1:
                self._queue = []
            else:
                self._queue = self._queue[1:]
        self._log.debug("removeNext: queue size now %d"%(len(self._queue), ))

    def addMessage(self, msg):
        if isinstance(msg, message.Message):
            self._queue.append(msg)
            self._log.debug("addMessage: queue size now %d"%(len(self._queue), ))

