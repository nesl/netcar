#!/usr/bin/env python
###########################################################################
# odb_io.py
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

import serial
import string
import time
from math import ceil

import obd_sensors
from powertrain_codes import pcodes
from network_codes    import ucodes
GET_DTC_COMMAND   = "03"
CLEAR_DTC_COMMAND = "04"

#__________________________________________________________________________
def decrypt_dtc_code(code):
    """Returns the 5-digit DTC code from hex encoding"""
    dtc = []
    current = code
    for i in range(0,3):
        if len(current)<4:
            raise "Tried to decode bad DTC: %s" % code

        tc = obd_sensors.hex_to_int(current[0]) #typecode
        tc = tc >> 2
        if   tc == 0:
            type = "P"
        elif tc == 1:
            type = "C"
        elif tc == 2:
            type = "B"
        elif tc == 3:
            type = "U"
        else:
            raise tc

        dig1 = str(obd_sensors.hex_to_int(current[0]) & 3)
        dig2 = str(obd_sensors.hex_to_int(current[1]))
        dig3 = str(obd_sensors.hex_to_int(current[2]))
        dig4 = str(obd_sensors.hex_to_int(current[3]))
        dtc.append(type+dig1+dig2+dig3+dig4)
        current = current[4:]
    return dtc
#__________________________________________________________________________


debug_file = open("obd_io_debug", "w")
def obd_debug(s):
    debug_file.write(str(s)+"\n")
    debug_file.flush()


class OBDPort:
     """ OBDPort abstracts all communication with OBD-II device."""
     def __init__(self,portnum):
         """Initializes port by resetting device and gettings supported PIDs. """
         # These should really be set by the user.
         baud     = 9600
         databits = 8
         par      = serial.PARITY_NONE  # parity
         sb       = 1                   # stop bits
         to       = 2

         try:
             self.port = serial.Serial(portnum,baud, \
             parity = par, stopbits = sb, bytesize = databits,timeout = to)
         except "FIXME": #serial.serialutil.SerialException:
             raise "PortFailed"

         obd_debug( self.port.portstr)
         ready = "ERROR"
         while ready == "ERROR":
             self.send_command("atz")   # initialize
             obd_debug( [self.get_result()])
             self.send_command("ate0")  # echo off
             obd_debug( [self.get_result()])
             self.send_command("0100")
	     ready = self.get_result()
	     print "DBG2: **%s**"%( ready.strip("\r"),)
	     if ready.find("UNABLE TO CONNECT") >= 0:
	     	print "Couldn't find Car... Retrying"
		ready = "ERROR"
	     else:
             	print "DBG: ", ready[-6:-1]
#
#         self.send_command( "0100")
#         obd_debug( [self.get_result()])
#         self.send_command( "0100")
#         obd_debug( [self.get_result()])
     
     def close(self):
         """ Resets device and closes all associated filehandles"""
         self.port.send_command("atz")
         self.port.close()
         self.port = None

     def send_command(self, cmd):
         """Internal use only: not a public interface"""
         if self.port:
             self.port.flushOutput()
             self.port.flushInput()
             for c in cmd:
                 self.port.write(c)
             self.port.write("\r")

     def interpret_result(self,code):
         """Internal use only: not a public interface"""
         # Code will be the string returned from the device.
         # It should look something like this:
         # '41 11 0 0\r\r'
         
         # 9 seems to be the length of the shortest valid response
         if len(code) < 7:
             raise "BogusCode"
          
         # get the first thing returned, echo should be off
         code = string.split(code, "\r")
         code = code[0]
         
         #remove whitespace
         code = string.split(code)
         code = string.join(code, "")
          

         if code[:6] == "NODATA": # there is no such sensor
             return "NODATA"
         # first 4 characters are code from ELM
         code = code[4:]
         return code
    
     def get_result(self):
         """Internal use only: not a public interface"""
         if self.port:
             buffer = ""
             while 1:
                 c = self.port.read(1)
		 if len(c) == 1:
		 	obd_debug(c)
		 	if c == '\r' and len(buffer) > 0 and buffer[-1] == '\r':
                     		break
                 	else:
                     		buffer = buffer + c
             return buffer
         return None

     # get sensor value from command
     def get_sensor_value(self,sensor):
         """Internal use only: not a public interface"""
         cmd = sensor.cmd
         self.send_command(cmd)
         data = self.get_result()
         if data:
             data = self.interpret_result(data)
             if data != "NODATA":
                 data = sensor.value(data)
         else:
             raise "NORESPONSE"
         return data

     # return string of sensor name and value from sensor index
     def sensor(self , sensor_index):
         """Returns 3-tuple of given sensors. 3-tuple consists of
         (Sensor Name (string), Sensor Value (string), Sensor Unit (string) ) """
         sensor = obd_sensors.SENSORS[sensor_index]
         try:
             r = self.get_sensor_value(sensor)
         except "NORESPONSE":
             r = "NORESPONSE"
         return (sensor.name,r, sensor.unit)

     def sensor_names(self):
         """Internal use only: not a public interface"""
         names = []
         for s in obd_sensors.SENSORS:
             names.append(s.name)
         return names


     #
     # fixme: j1979 specifies that the program should poll until the number
     # of returned DTCs matches the number indicated by a call to PID 01
     #
     def get_dtc(self):
          """Returns a list of all pending DTC codes. Each element consists of
          a 2-tuple: (DTC code (string), Code description (string) )"""
          r = self.sensor(1)
          num = r[0]
          # get all DTC, 3 per mesg response
          self.send_command(GET_DTC_COMMAND)
          #for i in range(0, ceil(num/3.0)):
          res = self.get_result()
          print res
          return res
              # fixme: finish

     def clear_dtc(self):
         """Clears all DTCs and freeze frame data"""
         self.send_command(CLEAR_DTC_COMMAND)     
         r = self.get_result()
         return r
     
     def log(self, sensor_index, filename): 
          file = open(filename, "w")
          start_time = time.time() 
          if file:
               data = self.sensor(sensor_index)
               file.write("%s     \t%s(%s)\n" % \
                         ("Time", string.strip(data[0]), data[2])) 
               while 1:
                    now = time.time()
                    data = self.sensor(sensor_index)
                    line = "%.6f,\t%s\n" % (now - start_time, data[1])
                    file.write(line)
                    file.flush()
          
          
# __________________________________________________________    
def test():
    p = OBDPort('/dev/tty.KeySerial1')
    supp =  p.sensor(0)[1]
    print supp
    
    r = p.get_dtc()
    print r
    #a =  decrypt_dtc_code("01430143C001")
    #print pcodes[a[0]]
    #print pcodes[a[1]]
    #print ucodes[a[2]]

def test_log():
     p = OBDPort('/dev/tty.KeySerial1')
     p.log(12, "logtest")
           


if __name__ == "__main__":
     test()
