import queue
import message
import time
import threading
import sys

#setup the logging system
import logging
logging.basicConfig()
log = logging.getLogger("DTNSendManager")
log.setLevel(logging.DEBUG)

class DTNSendManager(threading.Thread):
    """
    This is the Delay Tolerant Network Send Manager. It has a list of queues
    that it polls periodically. If there is something in the queue, it will
    send it to the server.
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self._queues = []
        pass

    def addQueue(self, q):
        """ Add a queue to the queuelist. """
        if isinstance(q, queue.Queue):
            log.debug("adding queue %s to the queue list."%(str(q),))
            self._queues.append(q)
    
    def run(self):
        """ This is the run method of the thread. """
        while 1:
            sentElement = False
            if len(self._queues) > 0:
                # iterate through all the queues
                for q in self._queues:
                    # if the queue isn't empty, send the data to the server.
                    if not q.isEmpty():
                        sentElement = True
                        log.debug("Preparing message: %s"%(q.getNext(),))
                        q.removeNext()
            if not sentElement:
                # we want to wait if we didn't send anything in order to not 
                # create a busy loop.
                log.debug("nothing to do...")
                time.sleep(1)


if __name__ == "__main__":
    log.info("Starting...")
    dtns = DTNSendManager()
    dtns.start()

    time.sleep(2)
    log.debug("Creating FIFOQueue")
    fq = queue.FIFOQueue()
    log.debug("Creating messages for queue")
    msg = message.Message(1, "testmessage")
    fq.addMessage(msg)
    dtns.addQueue(fq)
    
    time.sleep(5)
    log.debug("adding messages again...")
    fq.addMessage(msg)
    fq.addMessage(msg)
    fq.addMessage(msg)
