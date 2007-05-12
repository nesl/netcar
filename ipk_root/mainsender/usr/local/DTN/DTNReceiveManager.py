import socket
import os
import message
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
        self._s.bind((socket.gethostname(), port))
        self._s.listen(5)

        while 1:
            try:
                (c, addr) = self._s.accept()
            except KeyboardInterrupt:
                self._s.close()
                exit(0)
            if os.fork():
                #parent, close the connection
                c.close()
            else:
                #child, handle the connection
                self.handleConnection(c, addr)
                c.shutdown(2)
                exit(0)

    def registerModule(self, m):
        if isinstance(m, module.BaseModule):
            self._log.debug("Register module %s"%(m,))
            self._modules[m.getMessageType()] = m.getReceiveFunction()

    def handleConnection(self, socket, address):
        self.file = socket.makefile("rb")
        while 1:
            try:
                msg = message.Message(msg=self.file.readline().strip())
                # execute the registered callback function for the module.
                if msg.getType() in self._modules.keys():
                    self._modules[msg.getType()](msg)
                else:
                    self._log.debug("No module for type %d"%(msg.getType()))
                socket.send("OK\n")
                
            except KeyboardInterrupt:
                self.file.close()
                socket.shutdown(2)
                self._s.close()

                exit(0)
                
            self._log.info("Received message: %s"%(msg))
       

if __name__ == "__main__":

    dtnrm = DTNReceiveManager(PORT)
