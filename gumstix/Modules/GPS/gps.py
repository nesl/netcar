#!/usr/bin/python

# Copyright, 2006 Thomas Schmid (thomas.schmid[at]gmail.com)
# Copyright permissions given by the GPL Version 2.  http://www.fsf.org/

# Please see http://www.pygps.org for more information on how to use the NMEA object.

import string
import os, sys
from LatLongUTMconversion import LLtoUTM
import NMEA
import threading

#Logging setting
import logging

class GpsThread ( threading.Thread):
    # overwrite Thread's __init__ method
    def __init__(self, device):
        threading.Thread.__init__(self)
        self._device = device
        self._GPSFixNotificationFunctions = []
        self._log = logging.getLogger("GPS")
        self._log.setLevel(logging.DEBUG)
        self.semaphore = threading.Semaphore()
        self.semaphore.acquire()
        # init the nmea module
        try:
            self.__nmea = NMEA.NMEA()
            self.__nmea.speedunits = "%.2f mph"
            self.__nmea.speedmultiplier = 1.152
            self.__nmea.speed = 1
            self.__nmea.altitudemultiplier = 1.00
            self.__nmea.altitudeunits = "%.2f meters"
            self.__nmea.altitude = 5.7
        except:
            e = sys.exec_info()[1]
            self._log.error("error in __init__: "+str(e))
        self.semaphore.release()
        self.running = 1

    # handle input from gpsd.
    def gpsInput(self, line):
        self.semaphore.acquire()
        try:
            self.__nmea.handle_line(line)
            if self.__nmea.LATLON:
                self.__nmea.LATLON = 0

            if self.__nmea.SAT:
                self.__nmea.SAT = 0
            if self.__nmea.ZCH:
                self.__nmea.ZCH = 0
        except:
            e = sys.exec_info()[1]
            self._log.error("gpsInput: bad input: %s"%(e,)) 
        self.semaphore.release()

    def getCoordinates(self):
        self.semaphore.acquire()
        try:
            (long, lat, alt) = (self.__nmea.lat, self.__nmea.lon, self.__nmea.altitude)
        except:
            e = sys.exec_info()[1]
            self._log.error("getCoordinates: %s"%(e,)) 
        self.semaphore.release()
        return (long, lat, alt)

    def getTime(self):
        """ The time is in UTC! """
        self.semaphore.acquire()
        try:
            t = self.__nmea.time
        except:
            e = sys.exec_info()[1]
            self._log.error("getTime: %s"%(e,))
        
        self.semaphore.release()
        return t

    def getSpeed(self):
        self.semaphore.acquire()
        try:
            s = (self.__nmea.speedunits % (self.__nmea.speed * self.__nmea.speedmultiplier))
        except:
            e = sys.exec_info()[1]
            self._log.error("getSpeed: %s"%(e,))
            
        self.semaphore.release()
        return s
    
    def getSatellites(self):
        self.semaphore.acquire()
        try:
            s = self.__nmea.satellites
        except:
            e = sys.exec_info()[1]
            self._log.error("getSatellites: %s"%(e,))
        self.semaphore.release()
        return s
    
    def getSatelliteStatistics(self):
        self.semaphore.acquire()
        try:
            ss = list(self.__nmea.ss)
            prn = list(self.__nmea.prn)
            in_view = self.__nmea.in_view
        except:
            e = sys.exec_info()[1]
            self._log.error("getSatelliteStatistics: %s"%(e,))
        self.semaphore.release()
        return (ss, prn, in_view)

    # added to acquire PDOP(Younghun)
    def getPDOP(self):
        self.semaphore.acquire()
        try:
            s = self.__nmea.pdop
        except:
            e = sys.exec_info()[1]
            self._log.error("getPDOP: %s"%(e,))
        self.semaphore.release()
        return s
    
    def registerGPSFixNotificationFunction(self, f):
        self._GPSFixNotificationFunctions.append(f)

    def run(self):
        self._log.debug("in gps run")
        try:
            gpsdev = open(self._device)
        except :
            e = sys.exec_info()[1]
            self._log.error("run: %s"%(e,))
            self._log.error("exiting gps thread")
            return

        coordinates = (0, 0, 0)

        while self.running:
            try:
                line = gpsdev.readline()
                self.gpsInput(line)
                #check if it is different from the last fix:
                currentCoordinates = self.getCoordinates()
                if coordinates != currentCoordinates:
                    coordinates = currentCoordinates
                    for f in self._GPSFixNotificationFunctions:
                        # notify the registered functions of the change.
                        f(self)
            except:
                self._log.warning("decoded strange data. Error %s"%(e,))
                self._log.warning("string %s"%(line,))
            #print nmea.lat, nmea.lon, (nmea.speedunits % (nmea.speed * nmea.speedmultiplier))
            #print "time: %s UTC satelites: %d"%(nmea.time, nmea.satellites)
            #print nmea.ss, nmea.zs, nmea.zv

    def stop(self):
        self._log.debug("exit gps module")
        self.running=0
        sys.exit(1)
        
