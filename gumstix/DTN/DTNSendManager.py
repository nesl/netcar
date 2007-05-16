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

import queue
import message
import connection

from Modules import module

import time
import threading
import sys

#setup the logging system
import logging

#some configurations
SERVER = "suisse"
PORT = 14000

class DTNSendManager(threading.Thread):
    """
    This is the Delay Tolerant Network Send Manager. It has a list of queues
    that it polls periodically. If there is something in the queue, it will
    send it to the server.
    """
    def __init__(self, server, port, netcarID):
        threading.Thread.__init__(self)
        self._log = logging.getLogger("DTNSendManager")
        self._log.setLevel(logging.DEBUG)


        self._server = server
        self._port = port
        self._netcarID = netcarID
        self._queues = []
        self._connection = connection.SocketConnection(self._server, self._port, self._netcarID)

    def addQueue(self, q):
        """ Add a queue to the queuelist. """
        if isinstance(q, queue.Queue):
            self._log.debug("adding queue %s to the queue list."%(str(q),))
            self._queues.append(q)

    def registerModule(self, m):
        if isinstance(m, module.BaseModule):
            self.addQueue(m.getQueue())
            self._connection.registerModule(m)
    
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
                        self._log.debug("Preparing message: %s"%(q.getNext(),))
                        if self._connection.sendMessage(q.getNext()):
                            self._log.debug("Message successfully sent")
                            q.removeNext()
                        else:
                            self._log.debug("Couldn't send message")
            if not sentElement:
                # we want to wait if we didn't send anything in order to not 
                # create a busy loop.
                self._log.debug("nothing to do...")
                time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig()

    dtns = DTNSendManager(SERVER, PORT)
    dtns.start()

