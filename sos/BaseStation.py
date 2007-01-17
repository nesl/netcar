#!/usr/bin/python

import thread
import socket
import sys
import struct
import wx
import wx.lib.plot as plot

ACCELEROMETER_MODULE = 0x80

ACCELEROMETER_DATA = 41

SAMPLES_PER_MSG = 10

EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class SocketClient:
    """ """
    def __init__(self, host,port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected=1
        
        try:
            self.s.connect((host, port))
        except socket.error:
            self.connected=0
        self.data=""


    def close(self):
        if(self.connected):
            self.s.shutdown(2)
            self.s.close()

    def send(self, command):
        if(self.connected):
            self.s.send(command)
        else:
            print "Error: No connection to command server..."


class BaseStation(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(180, 280))

        self.client = plot.PlotCanvas(self)
        self.Show(True)

        self.index = 0
        self.d0 = []
        self.d1 = []
        
        EVT_RESULT(self,self.OnResult)

        self.sc = SocketClient("127.0.0.1", 7915)
        try:
            thread.start_new_thread(self.input_thread, ())
        except thread.error:
            print error

        try:
            thread.start_new_thread(self.output_thread, ())
        except thread.error:
            print error
        

    def OnResult(self, event):

        accel0 = event.data[0]
        accel1 = event.data[1]

        for i in range(len(accel0)):
            self.d0.append((self.index, accel0[i]))
            self.d1.append((self.index, accel1[i]))
            self.index+=1
            
        line0 = plot.PolyLine(self.d0, legend='accel0', colour='green', width=1)
        line1 = plot.PolyLine(self.d1, legend='accel1', colour='red', width=1)
        gc = plot.PlotGraphics([line0, line1], 'Line Graph', 'X Axis', 'Y Axis')
        self.client.Draw(gc, xAxis= (self.index-500, self.index), yAxis= (0,1024))
        
            
    def input_thread(self):
        print "Usage: if you want to send a T value to a node"
        print "       enter it as following and press enter:"
        print "       t <nodeid> <TValue>\n"
        print "       to send an alpha value to the processing"
        print "       module, enter it as following:"
        print "       a <nodeid> <alpha_value>\n"
        print "Note:  the client does not any checking on the values,"
        print "       thus please make sure that you enter only integers.\n"
        print "To exit, enter 'exit' and hit enter.\n"
        while 1:
            line = sys.stdin.readline().strip()
            print line
            if line == "exit":
                self.sc.close()
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
                    self.sc.send(message)
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
                    self.sc.send(message)

    def output_thread(self):
        lastdata = -1
        while 1:
            data = ord(self.sc.s.recv(1))
            #print data, ACCELEROMETER_MODULE
            if data == ACCELEROMETER_MODULE:
                (src_mod, dst_addr, src_addr, msg_type, msg_length) = struct.unpack("<BHHBB", self.sc.s.recv(7))
                #print src_mod, dst_addr, src_addr, msg_type, msg_length
                if msg_type == ACCELEROMETER_DATA:
                    accel0 = struct.unpack("<"+msg_length/4*'H', self.sc.s.recv(msg_length / 2))
                    accel1 = struct.unpack("<"+msg_length/4*'H', self.sc.s.recv(msg_length / 2))

                    wx.PostEvent(self, ResultEvent((accel0, accel1)))

                    print accel0
                    print accel1
                lastdata = -1
            else:
                lastdata = data

        
class MyApp(wx.App):
    def OnInit(self):
        frame = BaseStation(None, -1, 'Plotting')
        frame.Show(True)
        self.SetTopWindow(frame)
        
        return True
    
if(__name__ == "__main__"):

    app = MyApp(0)
    app.MainLoop()

