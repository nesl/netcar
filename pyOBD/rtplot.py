#!/usr/bin/env python

from wxPython.wx import * #fixme, for test only
from wxPython.lib import wxPlotCanvas 
from Queue import Queue

class RTPlot(wxPlotCanvas.PlotCanvas):
    class ringbuffer:
        def __init__(self, size):
            self.max = size
            self.data = []
        def add(self, point):
            # fixme, this sucks
            # linear time insert? FIX FIX FIX
            if len(self.data) >= self.max:
                for i in range(1,len(self.data)):
                    self.data[i-1] = self.data[i]
                self.data[-1] = point
            else:
                self.data.append(point)
        def get(self):
            return self.data
        
    def __init__(self, parent, id, size = 20):
        wxPlotCanvas.PlotCanvas.__init__(self,parent,id)
        self.data = Queue()
        self.buf = self.ringbuffer(20)
        
    def Plot(self):
        while 1:
            point  = self.data.get()
            print point
            self.buf.add(point)
            a = wxPlotCanvas.PolyMarker(self.buf.get())         
            self.draw(wxPlotCanvas.PlotGraphics([a]), 'automatic', 'automatic')

    def AddPoint(self, point):
        self.data.put(point)
        
def test():

    class junkprod:
        def __init__(self, plot):
            self.plot = plot
        def start(self):
            import time
            l = time.time()
            t = 0.0
            while 1:
                while t < l+1:
                    t = time.time()
                l = t
                self.plot.AddPoint((t+1,1))
                
    class TestApp(wxApp):
        def OnInit(self):
            import threading
            
            self.frame = wxFrame(NULL, -1, "Test RTPlot")
            self.frame.Show(true)

            id = wxNewId()
            self.p = RTPlot(self.frame, id)
            prod = junkprod(self.p)
            plotthread = threading.Thread(None, self.p.Plot, None, ())
            plotthread.start()

            prodthread = threading.Thread(None, prod.start, None, ())
            prodthread.start()


            return true

    app = TestApp(0)
    app.MainLoop()

if __name__ == "__main__":
    test()
