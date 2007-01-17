#!/usr/bin/python

import threading
import socket
import sys
import struct

ACCELEROMETER_MODULE = 0x80

ACCELEROMETER_DATA = 41

SAMPLES_PER_MSG = 10

class SocketClient(threading.Thread):
    """
    This class implements a threaded client. It sends a string to a
    server and the thread collects the data received in a variable.
    """
    def __init__(self, host,port):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected=1
        
        try:
            self.s.connect((host, port))
        except socket.error:
            self.connected=0
        self.data=""
        if(self.connected):
            self.start()

    def run(self):
        print "start receiving"
        try:
            lastdata = -1
            while 1:
                data = ord(self.s.recv(1))
                print data, ACCELEROMETER_MODULE
                if data == ACCELEROMETER_MODULE:
                    (src_mod, dst_addr, src_addr, msg_type, msg_length) = struct.unpack("BHHBB", self.s.recv(7))
                    print src_mod, dst_addr, src_addr, msg_type, msg_length
                    #if ms_gtype == ACCELEROMETER_DATA:
                    #    d = self.s.recv(msg_length)
                    #    print map(ord, d)
                    lastdata = -1
                else:
                    lastdata = data
        except:
            pass
        
    def close(self):
        if(self.connected):
            self.s.shutdown(2)
            self.s.close()

    def send(self, command):
        if(self.connected):
            self.s.send(command)
        else:
            print "Error: No connection to command server..."
        

if(__name__ == "__main__"):



    print "Usage: if you want to send a T value to a node"
    print "       enter it as following and press enter:"
    print "       t <nodeid> <TValue>\n"
    print "       to send an alpha value to the processing"
    print "       module, enter it as following:"
    print "       a <nodeid> <alpha_value>\n"
    print "Note:  the client does not any checking on the values,"
    print "       thus please make sure that you enter only integers.\n"
    print "To exit, enter 'exit' and hit enter.\n"
    sc = SocketClient("127.0.0.1", 7915)
    while 1:
        line = sys.stdin.readline().strip()
        print line
        if line == "exit":
            sc.close()
            sys.exit()

        splittedline = line.split()
        if len(splittedline) == 3:
            if splittedline[0] == "t":
                try:
                    nodeid = int(splittedline[1])
                except:
                    print "Error: nodeid is not an integer\n"
                    continue
                try:
                    value = int(splittedline[2])
                except:
                    print "Error: t-vale is not an integer\n"
                    continue
                
                message = "" + chr(PROCESSING_MODULE) + chr(PROCESSING_MODULE) #did, sid
                message += chr(nodeid%256) + chr(nodeid/256) #daddr
                message += chr(UART_ADDR%256) + chr(UART_ADDR/256) #saddr
                message += chr(T_PARAM) #msg type MSG_DATA_SET_PARAM
                message += chr(2) #data len
                message += chr(value%256) + chr(value/256)
                print "sending message to nodeid %s value %d"%(nodeid, value)
                sc.send(message)
            elif splittedline[0] == "a":
                try:
                    nodeid = int(splittedline[1])
                except:
                    print "Error: nodeid is not an integer\n"
                    continue
                try:
                    value = float(splittedline[2])
                except:
                    print "Error: alpha is not a double between 0 and 1\n"
                    continue
                if value < 0:
                    print "Error: alpha value can't be <0\n"
                    continue
                if value > 1:
                    print "Error: alpha value can't be > 0\n"
                    continue

                #discretize the value into 16bit
                value = int(value*((1<<16)-1))
                
                message = "" + chr(PROCESSING_MODULE) + chr(PROCESSING_MODULE) #did, sid
                message += chr(nodeid%256) + chr(nodeid/256) #daddr
                message += chr(UART_ADDR%256) + chr(UART_ADDR/256) #saddr
                message += chr(ALPHA_PARAM) #msg type MSG_DATA_SET_PARAM
                message += chr(2) #data len
                message += chr(value%256) + chr(value/256)
                print "sending message to nodeid %s value %d (discretized to 16bit)"%(nodeid, value)
                sc.send(message)

