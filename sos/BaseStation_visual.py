#!/usr/bin/python

import thread
import socket
import sys
import struct
import time
import wx
import wx.lib.plot as plot

ACCELEROMETER_MODULE = 0x80

ACCELEROMETER_DATA = 33

SAMPLES_PER_MSG = 20
SAMPLE_RATE = 50

EVT_RESULT_ID = wx.NewId()

ID_CONNECT = 101
ID_EXIT = 110
ID_PLOT = 102

collist = ['green',
           'red',
           'blue',
           'cyan']

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

        # Setting up the menu
        filemenu = wx.Menu()
        filemenu.Append(ID_CONNECT, "&Connect", " Connect to a live stream of data")
        filemenu.Append(ID_PLOT, "&Plot", " Plot an existing stream of data from a file")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit", " Terminate the program")
        # Creating the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&Menu") # Adding the "filemenu" to menubar
        self.SetMenuBar(menuBar) # Adding menubar to the frame content

        #Sending events on "Connect" "Plot" and "Exit"
        wx.EVT_MENU(self, ID_CONNECT, self.OnConnect)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_PLOT, self.OnPlot)

        self.client = plot.PlotCanvas(self)
        self.client.SetEnableLegend(True)
        self.Show(True)

        self.index = 0
        self.d0 = {}
        self.d1 = {}

        EVT_RESULT(self,self.OnResult)

    # Handlers for events on "Connect" "Plot" and "Exit"
    def OnConnect(self, e):
        d = wx.MessageDialog(self, "Hit Connect"
                             " in python", "blah", wx.OK)
        d.ShowModal()
        d.Destroy()
        self.sc = SocketClient("127.0.0.1", 7915)
        try:
            thread.start_new_thread(self.input_thread, ())
        except thread.error:
            print error

        try:
            thread.start_new_thread(self.output_thread, ())
        except thread.error:
            print error
    def OnPlot(self, e):
        d = wx.MessageDialog(self, "Hit Plot"
                             " in python", "blah", wx.OK)
        d.ShowModal()
        d.Destroy()

    def OnExit(self, e):
        self.Close(True)

    def OnResult(self, event):

        src_addr = event.data['src_addr']
        accel0 = event.data['accel0']
        accel1 = event.data['accel1']

        if src_addr not in self.d0.keys():
            self.d0[src_addr] = []
            self.d1[src_addr] = []
        self.d0[src_addr] += accel0
        self.d1[src_addr] += accel1
        self.d0[src_addr][0:max(-600, -len(self.d0[src_addr]))] = []
        self.d1[src_addr][0:max(-600, -len(self.d1[src_addr]))] = []
        lines = []
        i=0
        for src_addr in self.d0.keys():
            lines.append(plot.PolyLine(self.d0[src_addr], legend=str(src_addr)+' accel0', colour=collist[i], width=1))
            lines.append(plot.PolyLine(self.d1[src_addr], legend=str(src_addr)+' accel1', colour=collist[i], width=1))
            i += 1
        gc = plot.PlotGraphics(lines, 'Accelerations', 'Time [s]', 'Acceleration 10bit')
        # the X axis shows the last 500 samples
        self.client.Draw(gc, xAxis= (self.d0[src_addr][max(-500, -len(self.d0[src_addr]))][0], self.d0[src_addr][-1][0]), yAxis= (0,1024))



    def input_thread(self):
        """ currently we don't use the input thread.
        """
        pass

    def output_thread(self):
        lastdata = -1
        nodes = {}
        start_time = time.time()
        while 1:
            data = ord(self.sc.s.recv(1))
            #print data, ACCELEROMETER_MODULE
            if data == ACCELEROMETER_MODULE:
                time_rx = time.time()
                try:
                    s = self.sc.s.recv(7)
                    (src_mod, dst_addr, src_addr, msg_type, msg_length) = struct.unpack("<BHHBB", s)
                except struct.error:
                    print struct.error
                    print "bad msg header:", map(ord, s)
                #print src_mod, dst_addr, src_addr, msg_type, msg_length
                if msg_type == ACCELEROMETER_DATA:
                    try:
                        s = self.sc.s.recv(4)
                        # remove the 4 time bytes from the message length
                        msg_length -= 4
                        (time_rx, ) = struct.unpack("<L", s)
                        time_rx /= 115200.0
                    except struct.error:
                        print struct.error
                        print "bad string for time:", map(ord, s)
                    
                    try:
                        s = self.sc.s.recv(SAMPLES_PER_MSG*2)
                        accel0 = struct.unpack("<"+msg_length/4*'H', s)
                    except struct.error:
                        print struct.error
                        print "bad string for accel0:", map(ord, s)
                    try:
                        s = self.sc.s.recv(SAMPLES_PER_MSG*2)
                        accel1 = struct.unpack("<"+msg_length/4*'H', s)
                    except struct.error:
                        print struct.error
                        print "bad string for accel1:", map(ord, s)

                    #try to find out the sample times
                    if src_addr not in nodes.keys():
                        #never seen the node before.
                        nodes[src_addr] = {'last_seen': time_rx, 'file': open(str(src_addr)+".log", 'w')}

                    else:
                        d0 = []
                        d1 = []

                        # correlate the samples with time
                        # FIXME: this is only an estimate based on the reception time of the sample.
                        for i in range(len(accel0)):
                            t = time_rx - (SAMPLES_PER_MSG-i)*1/float(SAMPLE_RATE)
                            d0.append((t, accel0[i]))
                            d1.append((t, accel1[i]))
                            nodes[src_addr]['file'].write('%f\t%d\t%d\n'%(time_rx - (SAMPLES_PER_MSG-i)*1/float(SAMPLE_RATE), accel0[i], accel1[i]))

                        nodes[src_addr]['last_seen'] = time_rx
                        wx.PostEvent(self, ResultEvent({'src_addr': src_addr, 'accel0': d0, 'accel1': d1}))

                    #print accel0
                    #print accel1
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

