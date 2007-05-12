import socket
import os
import sys
import message
import struct
from Modules import module

import logging
logging.basicConfig()

PORT = 14000

class DTNReceiveManager:
    """
        This is the Delay Tolerant Network Receive Manager. The DTNSRM
        listens on a TCP port for incomming connections from a DTNSM and
        decodes its messages. It will then dispatch these messages
        according to their message type.
    """
    def __init__(self, port):
        self._log = logging.getLogger("DTNReceiveManager")
        self._log.setLevel(logging.DEBUG)

        self._modules = {}

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self._s.bind((socket.gethostname(), port))
        self._s.bind(("", port))

    def start(self):
        self._s.listen(5)

        while 1:
            try:
                (c, addr) = self._s.accept()
            except KeyboardInterrupt:
                self._s.close()
                sys.exit(0)
            if os.fork():
                #parent, close the connection
                c.close()
            else:
                #child, handle the connection
                self.handleConnection(c, addr)
                c.shutdown(2)
                sys.exit(0)

    def registerModule(self, m):
        if isinstance(m, module.BaseModule):
            self._log.debug("Register module %s"%(m,))
            self._modules[m.getMessageType()] = m.getReceiveFunction()

    def handleConnection(self, socket, address):
        while 1:
            try:
                while 1:
                    c = socket.recv(1)
                    if c == "#":
                        c = socket.recv(1)
                        if c == "$":
                            c = socket.recv(1)
                            if c == "*":
                                #found start of frame delimiter!
                                break
                header = ""
		while len(header) < struct.calcsize("!BH"):
		    header += socket.recv(1)
                (type, length) = struct.unpack("!BH", header)
		msg = ""
		while len(msg) < length:
		    msg += socket.recv(1)
                # execute the registered callback function for the module.
                if type in self._modules.keys():
                    self._modules[type](msg)
                else:
                    self._log.debug("No module for type %d"%(type))
                #socket.send("OK\n")
                
            except KeyboardInterrupt:
                socket.shutdown(2)
                self._s.close()

                sys.exit(0)
                
            self._log.info("Received message: %s"%(msg))
       

if __name__ == "__main__":

    dtnrm = DTNReceiveManager(PORT)
