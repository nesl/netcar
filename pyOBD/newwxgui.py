#!/usr/local/bin/env pythonw
############################################################################
#
# wxgui.py
#
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
############################################################################

import obd_io

import threading
from wx import *
from lib.mixins.listctrl import wxListCtrlAutoWidthMixin

ID_ABOUT  = 101
ID_EXIT   = 110
ID_CONFIG = 500
ID_CLEAR  = 501
ID_GETC   = 502
ID_RESET  = 503
ID_LOOK   = 504
ALL_ON    = 505
ALL_OFF   = 506


class MyApp(wxApp):
    # A listctrl which auto-resizes the column boxes to fill
    class MyListCtrl(wxListCtrl, wxListCtrlAutoWidthMixin):
        def __init__(self, parent, id, pos = wxDefaultPosition,
                     size = wxDefaultSize, style = 0):
            wxListCtrl.__init__(self,parent,id,pos,size,style)
            wxListCtrlAutoWidthMixin.__init__(self)
                
    class sensorProducer:
        def __init__(self, p,listctrl):
            from Queue import Queue
            self.list     = listctrl
            self.port     = p
            self.active   = []
            self.supp     = p.sensor(0)[1]
            for i in range(0, len(self.supp)):
                if self.supp[i] == "1":
                    self.active.append(1)
                else:
                    self.active.append(1)
                
            self.done = Queue(1) # signal the producer to finish
                    
        def start(self):
            while self.done.empty():
                for i in range(3, len(self.active)):
                    if self.active[i]:
                        s = self.port.sensor(i)
                        print i,s
                        self.list.SetStringItem(i, 2, "%s (%s)" % (s[1], s[2]))
                        self.list.SetStringItem(i, 0, "1")
                    if not self.done.empty():
                        break
            self.done.get()

        def stop(self):
            self.done.put(1)

    def sensor_control_on(self):
        self.all_on_but.Enable(True)
        self.all_off_but.Enable(True)
        self.senmenu.Enable(ALL_ON ,True)
        self.senmenu.Enable(ALL_OFF,True)
        self.dtcmenu.Enable(ID_GETC,True)
        self.dtcmenu.Enable(ID_CLEAR,True)

    def sensor_control_off(self):
        self.all_on_but.Enable(False)
        self.all_off_but.Enable(False)
        self.senmenu.Enable(ALL_ON ,False)
        self.senmenu.Enable(ALL_OFF,False)
        self.dtcmenu.Enable(ID_GETC,False)
        self.dtcmenu.Enable(ID_CLEAR,False)
        
    def all_sensors_on(self,  e = None):
        print "All on!"
    def all_sensors_off(self, e = None):
        print "All off!"
                
    def build_sensor_page(self):
        HOFFSET_LIST=30
        tID = wxNewId()

        panel = wxPanel(self.nb, -1)

        self.all_on_but  = wxButton(panel,ALL_ON ,"All On" , wxPoint(15,0))
        self.all_off_but = wxButton(panel,ALL_OFF,"All Off", wxPoint(100,0))

        EVT_BUTTON(panel, ALL_ON,  self.all_sensors_on)
        EVT_BUTTON(panel, ALL_OFF, self.all_sensors_off)
        
        self.sensors = self.MyListCtrl(panel, tID, pos=wxPoint(0,HOFFSET_LIST),
                                  style=
                                  wxLC_REPORT     |  
                                  wxSUNKEN_BORDER |
                                  wxLC_HRULES     |
                                  wxLC_SINGLE_SEL)
     

        self.sensors.InsertColumn(0, "Active",width=100)
        self.sensors.InsertColumn(1, "Sensor",format=wxLIST_FORMAT_RIGHT, width=250)
        self.sensors.InsertColumn(2, "Value", width=150)
        for i in range(0, len(obd_io.obd_sensors.SENSORS)):
            s = obd_io.obd_sensors.SENSORS[i].name
            self.sensors.InsertStringItem(i, "")
            self.sensors.SetStringItem(i, 0, "0")
            self.sensors.SetStringItem(i, 1, s)
            
            
        ####################################################################
        # This little bit of magic keeps the list the same size as the frame
        def OnPSize(e, win = panel):
            panel.SetSize(e.GetSize())
            self.sensors.SetSize(e.GetSize())
            w,h = self.frame.GetClientSizeTuple()
            # I have no idea where 70 comes from
            self.sensors.SetDimensions(0,HOFFSET_LIST, w-16 , h - 70 )

        EVT_SIZE(panel, OnPSize)
        ####################################################################

        self.nb.AddPage(panel, "Sensors")
                
    def OnInit(self):
        self.COMPORT = 0
        self.senprod = None

        tID = wxNewId()
                
        frame = wxFrame(NULL, -1, "pyOBD-II")
        self.frame=frame

        # Main notebook frames
        self.nb  = wxNotebook(frame, -1, style = wxNB_TOP)
        self.build_sensor_page()

        self.dtc = self.MyListCtrl(self.nb, tID,style=wxLC_REPORT|wxSUNKEN_BORDER)
        self.dtc.InsertColumn(0, "Code", width=100)
        self.dtc.InsertColumn(1, "Diagnosis", width=420)
        self.nb.AddPage(self.dtc, "DTC")

        # Setting up the menu.
        filemenu= wxMenu()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")

        settingmenu = wxMenu()
        settingmenu.Append(ID_CONFIG,"Configure"," Configure pyOBD")
        settingmenu.Append(ID_RESET,"Reset"," Reopen and reset device")

        senmenu= wxMenu()
        self.senmenu = senmenu
        senmenu.Append(ALL_ON  ,"All On"," Turn all sensors on")
        senmenu.Append(ALL_OFF ,"All Off"," Turn all sensors off")

        dtcmenu= wxMenu()
        self.dtcmenu = dtcmenu
        dtcmenu.Append(ID_GETC  ,"Get DTCs"," Get DTC Codes")
        dtcmenu.Append(ID_CLEAR ,"Clear DTC"," Clear DTC Codes")
        dtcmenu.Append(ID_LOOK  ,"Code Lookup"," Lookup DTC Codes")

        # Creating the menubar.
        menuBar = wxMenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(settingmenu,"&Settings")
        menuBar.Append(senmenu,"&Sensors")
        menuBar.Append(dtcmenu,"&DTC")
        
        frame.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        EVT_MENU(frame, ID_EXIT, self.OnExit)   # attach the menu-event ID_EXIT to the
        EVT_MENU(frame, ID_CLEAR , self.QueryClear)   
        EVT_MENU(frame, ID_CONFIG, self.Configure)
        EVT_MENU(frame, ALL_ON   , self.all_sensors_on)
        EVT_MENU(frame, ALL_OFF  , self.all_sensors_off)   
        EVT_MENU(frame, ID_RESET , self.OpenPort)
        EVT_MENU(frame, ID_GETC  , self.GetDTC)
        EVT_MENU(frame, ID_LOOK  , self.CodeLookup)   
  
        self.SetTopWindow(frame)
        self.AddDTC(["P0001",obd_io.pcodes["P0001"]])
        self.AddDTC(["P0002",obd_io.pcodes["P0002"]])
        self.AddDTC(["P0004",obd_io.pcodes["P0004"]])
        self.AddDTC(["P0005",obd_io.pcodes["P0005"]])
        self.AddDTC(["P0006",obd_io.pcodes["P0006"]])
        self.AddDTC(["P0002",obd_io.pcodes["P0002"]])
        self.AddDTC(["P0003",obd_io.pcodes["P0003"]])
        self.AddDTC(["P0300",obd_io.pcodes["P0300"]])

        frame.Show(true)
        frame.SetSize((500,400))
        self.sensor_control_off()
        return true

    def OpenPort(self,e):
        print "OpenPort called"
        self.port = obd_io.OBDPort(self.COMPORT)

        if self.senprod: # signal current producers to finish
            self.senprod.stop()
        self.senprod = self.sensorProducer(self.port, self.sensors) 
        self.sensthread = threading.Thread(None, self.senprod.start, None, ())
        self.sensthread.start()

        self.sensor_control_on()
        

    def GetDTC(self,e):
        print "GetDTC called"
        
    def AddDTC(self, code):
        self.dtc.InsertStringItem(0, "")
        self.dtc.SetStringItem(0, 0, code[0])
        self.dtc.SetStringItem(0, 1, code[1])


    def CodeLookup(self,e):
        id = 0
        diag = wxDialog(self.frame, id, title="Diagnosis Trouble Codes")

        sizer = wxBoxSizer(wxVERTICAL)

        tree = wxTreeCtrl(diag, id, style = wxTR_HAS_BUTTONS)
        proot = tree.AddRoot("Powertrain (P)Codes")
        tree.AppendItem(proot, "ASDFASDF")
        uroot = tree.AddRoot("Netork (U) Codes")


        sizer.Add(tree,0)
        box  = wxBoxSizer(wxHORIZONTAL)
        box.Add(wxButton(diag,wxID_OK,     "Ok"    ),0)
        box.Add(wxButton(diag,wxID_CANCEL, "Cancel"),0)

        sizer.Add(box, 0)
        diag.SetSizer(sizer)
        diag.SetAutoLayout(True)
        sizer.Fit(diag)
        r  = diag.ShowModal()
            
    def QueryClear(self,e):
        id = 0
        diag = wxDialog(self.frame, id, title="Clear DTC?")

        sizer = wxBoxSizer(wxVERTICAL)
        sizer.Add(wxStaticText(diag, -1, "Are you sure you wish to"),0)
        sizer.Add(wxStaticText(diag, -1, "clear all DTC codes and "),0)
        sizer.Add(wxStaticText(diag, -1, "freeze frame data?      "),0)
        box  = wxBoxSizer(wxHORIZONTAL)
        box.Add(wxButton(diag,wxID_OK,     "Ok"    ),0)
        box.Add(wxButton(diag,wxID_CANCEL, "Cancel"),0)

        sizer.Add(box, 0)
        diag.SetSizer(sizer)
        diag.SetAutoLayout(True)
        sizer.Fit(diag)
        r  = diag.ShowModal()
        if r == wxID_OK:
            self.ClearDTC()

    def ClearDTC(self):
        self.dtc.DeleteAllItems()


    def Configure(self,e):
        id = 0
        diag = wxDialog(self.frame, id, title="Configure")
        sizer = wxBoxSizer(wxVERTICAL)

        ports = ['COMM 1', 'COMM 2', 'COMM 3', 'COMM 4',
                 'COMM 5', 'COMM 6', 'COMM 7', 'COMM 8'] 
        rb = wxRadioBox(diag, id, "Choose Serial Port",
                        choices = ports, style = wxRA_SPECIFY_COLS,
                        majorDimension = 2)
        sizer.Add(rb, 0)
        
        box  = wxBoxSizer(wxHORIZONTAL)
        box.Add(wxButton(diag,wxID_OK,     "Ok"    ),0)
        box.Add(wxButton(diag,wxID_CANCEL, "Cancel"),0)

        sizer.Add(box, 0)
        diag.SetSizer(sizer)
        diag.SetAutoLayout(True)
        sizer.Fit(diag)
        r  = diag.ShowModal()
        if r == wxID_OK:
            self.COMPORT = rb.GetSelection()

    def OnExit(self,e = None):
        import sys
        sys.exit(0)

app = MyApp(0)
app.MainLoop()
