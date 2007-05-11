"""
  Copyright (c) 2003 The Regents of the University of California.
  All rights reserved.
 
  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions
  are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above
     copyright notice, this list of conditions and the following
     disclaimer in the documentation and/or other materials provided
     with the distribution.
  3. Neither the name of the University of California nor the names of
     its contributors may be used to endorse or promote products derived 
     from this software without specific prior written permission.
 
  THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
  PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS
  OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
  USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
  OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
  SUCH DAMAGE.


  @author Thomas Schmid <thomas.schmid@ucla.edu>
"""

import Queue as pyQueue
import message
import threading

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
        self._queueSemaphore = threading.Semaphore()
    
    def isEmpty(self):
        self._log.debug("in isEmpty")
        self._queueSemaphore.acquire()
        ret = False
        if len(self._queue) == 0:
            ret = True
        self._queueSemaphore.release()
        return ret

    def getNext(self):
        ret = None
        if not self.isEmpty():
            self._queueSemaphore.acquire()
            ret = self._queue[0]
            self._queueSemaphore.release()
        return ret

    def removeNext(self):
        if not self.isEmpty():
            self._queueSemaphore.acquire()
            if len(self._queue) == 1:
                self._queue = []
            else:
                self._queue = self._queue[1:]
            self._queueSemaphore.release()
        self._log.debug("removeNext: queue size now %d"%(len(self._queue), ))

    def addMessage(self, msg):
        if isinstance(msg, message.Message):
            self._queueSemaphore.acquire()
            self._queue.append(msg)
            self._queueSemaphore.release()
            self._log.debug("addMessage: queue size now %d"%(len(self._queue), ))

