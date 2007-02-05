#!/usr/bin/env python
############################################################################
#
# cursesgui.py
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
###########################################################################

import curses
import time
import sys

import threading
from Queue import Queue
from Queue import Empty

import obd_io

MAIN_MENU = [
    " 1: Read/Clear Diagnostic Trouble Codes",
    " 2: Display Engine Sensor Data",
    " 3: Open Port",
    " q: Quit to Multics"
    ]

DTC_CLEAR_WARNING = [
    " Are you SURE you wish to clear all",
    " DTC codes and freeze frame data?  ",
    " (Y/N)?                            "
    ]

debug_file = open("curses_debug", "w")

def debug(str):
    debug_file.write(str+"\n")
    debug_file.flush()

class CursesGui:

    # class to read from the console and put commands in the
    # command queue
    class cmdProducer:
        def __init__(self):
            self.queue    = Queue(1)
            self.done     = Queue(1) # signal the producer to finish

        def start(self,scr):
            while  self.done.empty():
                c = scr.getch()
                self.queue.put(c)
                # Fixme, race between producer and consumer
                time.sleep(.01)
            self.done.get()

    class sensorProducer:
        def __init__(self,p):
            self.port     = p
            self.queue    = []
            self.supp = p.sensor(0)[1]
            self.supp = self.supp
            for i in range(3, len(self.supp)):
                if self.supp[i] == "1":
                    active = 1
                else:
                    active = 0
                sensor_item = [active, Queue(1)]
                self.queue.append(sensor_item)
            self.done     = Queue(1) # signal the producer to finish
            
        def start(self):
            while self.done.empty():
                for i in range(3, len(self.queue)):
                    if self.queue[i][0] == 1:
                        s = self.port.sensor(i)
                        debug(str(s))
                        self.queue[i][1].put(s)
                    if not self.done.empty():
                        break
            self.done.get()


    def open_port(self,scr):
        port = 0
        try:
            self.port = obd_io.OBDPort(port)
        except "PortFailed":
            self.port = None
            self.popup("Could not open port %d" % port,scr)
        else:
            self.sensorqueue = self.sensorProducer(self.port)

    def popup(self, mesg, scr):

        h = scr.getmaxyx()[0]
        w = scr.getmaxyx()[1]
        if type(mesg) == str:
            win = curses.newwin(1, len(mesg)+1, h / 2, (w/2) - len(mesg)/2)
            win.addstr(0, 0,  mesg,curses.A_REVERSE)
        elif type(mesg) == list:
            start = (h / 2) - (len(mesg) / 2) 
            win = curses.newwin(start, len(mesg[0])+1, start, (w/2) - len(mesg[0])/2)
            for i in range(0, len(mesg)):
                win.addstr(i, 0,  mesg[i],curses.A_REVERSE)

        win.refresh()
        scr.refresh()
        return self.cmd_queue.queue.get()        

    def draw_border(self,scr):
        scr.clear()
        scr.border()
        scr.addstr(0, scr.getmaxyx()[1]-9, " pyODB ")
        scr.refresh()
        
    def draw_sensors(self,scr):

        voffset = -2  # vertical offset
        hoffset =  2  # horizontal offset

        scr.addstr(0, hoffset, " q: back ")

        sensor_names = self.port.sensor_names()
        for i in range(3,len(self.sensorqueue.queue)):
            s = "[%d] %s" % (self.sensorqueue.queue[i][0], sensor_names[i])
            scr.addstr(voffset+i, hoffset, s)
        scr.refresh()

        for i in range(3,len(self.sensorqueue.queue)):
            try:
                line = (self.sensorqueue.queue[i])[1].get_nowait()
            except Empty:
                continue
            else:
                hoffset = 5 + len(sensor_names[i]) + 2           
                line = "%s %s" % (str(line[1]), line[2])
                scr.addstr(voffset+i, hoffset, line)
                scr.refresh()
                
        scr.refresh()

    def show_sensors(self,scr):
        if self.port:
            self.sensor_thread = threading.Thread(None, self.sensorqueue.start, None, ()) 
            self.sensor_thread.start()
            
            self.draw_border(scr)
            c = "" # continue
            while c != ord('q'):
                c = ""
                self.draw_sensors(scr)
                try:
                    c = self.cmd_queue.queue.get_nowait()
                except Empty:
                    pass
                if c == 10: # Enter key
                    return
                time.sleep(.05)

            self.sensorqueue.done.put(1)
            self.sensor_thread.join()
        else:
            self.popup("No port available!",scr)
            

    def manage_dtc(self,scr):
        c = "" # continue
        while c != ord('q'):
            c = ""

            self.draw_border(scr)
            scr.addstr(scr.getmaxyx()[0]-2,3, "c: Clear All DTC Codes")
            scr.addstr(3,3, "Reading DTC codes is not yet supported")
            scr.refresh()
            c = self.cmd_queue.queue.get()
            if c == ord('c'):
                r = self.popup(DTC_CLEAR_WARNING,scr)
                if r == ord('y') or r == ord('Y'):
                    if self.port:
                        r = port.clear_dtc()
                    else:
                        self.draw_border(scr)
                        self.popup(" No Port Available!", scr)             
                    
        
    def draw_main_window(self,scr):
        self.draw_border(scr)
        
        voffset = 1 # offset from top of screen for menu
        hoffset = 2 # offset from left border
        for i in range(0,len(MAIN_MENU)):
            line = MAIN_MENU[i]
            if self.main_selected == i:
                style = curses.A_REVERSE
            else:
                style = curses.A_NORMAL
            scr.addstr(voffset+i, hoffset, line,style)

        scr.refresh()

    def main_loop(self,scr):
        self.cmd_thread= threading.Thread(None, self.cmd_queue.start, None, (scr,)) 
        self.cmd_thread.start()

        #self.open_port(scr)

        c = "" # continue
        while c != ord('q'):
            self.draw_main_window(scr)
            c = self.cmd_queue.queue.get()
            if   c == curses.KEY_DOWN:
                if not self.main_selected >= len(MAIN_MENU)-1:
                    self.main_selected += 1
            elif c == curses.KEY_UP:
                if(not self.main_selected <= 0):
                    self.main_selected -= 1
            elif c == ord('1'):
                    self.manage_dtc(scr)
            elif c == ord('2'):
                self.show_sensors(scr)
            elif c == ord('3'):
                self.open_port(scr)

            elif c == 10: # Enter key
                if self.main_selected == 0:
                    self.manage_dtc(scr)
                elif self.main_selected == 1:
                    self.show_sensors(scr)
                elif self.main_selected == 2:
                    self.open_port(scr)
                elif self.main_selected == 3:
                    break


        self.cmd_queue.done.put(1)
        self.cmd_thread.join()


    def __init__(self):
        self.port = None
        self.main_selected = 0
        self.cmd_queue   = self.cmdProducer()

    def start(self):
        debug("starting")
        curses.initscr()

        # for some reason unknown to me, this crashes macs
        if sys.platform != "darwin":
            curses.curs_set(0)

        curses.wrapper(self.main_loop)
        
# __________________________________________________________    
def test():
    interface = CursesGui()
    interface.start()

if __name__ == "__main__":
    test()
