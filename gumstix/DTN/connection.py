import socket
import time
import logging
import message

from Modules import module

class Connection:
    """
        This class is a generic example for a connection. Future connection
        classes should inherit from this one.
    """
    def __init__(self):
        self._log = logging.getLogger("Connection")
        self._log.setLevel(logging.DEBUG)

        self._modules = {}

    def sendMessage(self, msg):
        self._log.debug("Sending message %s"%(msg,))

    def registerModule(self, m):
        if isinstance(m, module.BaseModule):
            self._log.debug("Register module %s"%(m,))
            self._modules[m.getMessageType()] = m.getReceiveFunction()

class SocketConnection(Connection):
    """
        This class implements a socket connection to a server.
    """
    def __init__(self, server, port):
        Connection.__init__(self)
        self._log = logging.getLogger("SocketConnection")
        self._log.setLevel(logging.DEBUG)

        self._SFD = "#$*"

        self._server = server
        self._port = port

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #set the timeout of the socket
        self._s.settimeout(5.0)

        self._connected = False

    def sendMessage(self, msg):
        """ Send a message to the server. If the connection doesn't exist yet, 
        this method will try to establish it first.

        Returns False if the send failed, True if it was successfull.
        """
        while not self._connected:
            if not self.connect():
                # sleep for a little to avoid a busy loop
                time.sleep(0.5)
        try:
            # send the message encapsulated into a normal message.
            self._s.send(self._SFD + message.Message(msgType=msg.getType(), content=msg.encode()).encode())
            #line = self._file.readline().strip()
            #if line != "OK":
            #    return False
            return True
        except socket.error, e:
            self._log.error("sendMessage: SocketError: "+str(e))
            if e[0] == 32:
                #Broken Pipe error. Invalidate the connection.
                self._log.error("sendMessage: invalidating connection")
                self._connected = False

        return False

    def connect(self):
        """ Connect to the server and do error handling if the connection failed. """
        try:
            #make sure an old connection is closed.
            self._s.close()
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #set the timeout of the socket
            self._s.settimeout(5.0)
            self._s.connect((self._server, self._port))
            self._file = self._s.makefile("rb")
            self._connected = True
            return True
        except socket.error, e:
            self._log.error("connect: SocketError: "+str(e))
            return False

