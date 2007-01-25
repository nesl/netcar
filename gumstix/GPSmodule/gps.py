#!/usr/bin/python

# Copyright, 2006 Thomas Schmid (thomas.schmid[at]gmail.com)
# Copyright permissions given by the GPL Version 2.  http://www.fsf.org/

# Please see http://www.pygps.org for more information on how to use the NMEA object.

import socket, string
import os, sys
from LatLongUTMconversion import LLtoUTM
import NMEA
import threading


class GpsThread ( threading.Thread):
    # overwrite Thread's __init__ method
    def __init__(self):
        # init the nmea module
        self.semaphore = threading.Semaphore()
        self.semaphore.acquire()
        
        self.__nmea = NMEA.NMEA()
        self.__nmea.speedunits = "%.2f mph"
        self.__nmea.speedmultiplier = 1.152
        self.__nmea.speed = 1
        self.__nmea.altitudemultiplier = 1.00
        self.__nmea.altitudeunits = "%.2f meters"
        self.__nmea.altitude = 5.7

        self.semaphore.release()
        self.running = 1
        #call the super constructor
        threading.Thread.__init__(self)

    # handle input from gpsd.
    def gpsInput(self, line):
        self.semaphore.acquire()
        self.__nmea.handle_line(line)
        if self.__nmea.LATLON:
            self.__nmea.LATLON = 0

        if self.__nmea.SAT:
            self.__nmea.SAT = 0
        if self.__nmea.ZCH:
            self.__nmea.ZCH = 0
        self.semaphore.release()

    def getCoordinates(self):
        self.semaphore.acquire()
        (long, lat) = (self.__nmea.lat, self.__nmea.lon)
        self.semaphore.release()
        return (long, lat)

    def getTime(self):
        """ The time is in UTC! """
        self.semaphore.acquire()
        t = self.__nmea.time
        self.semaphore.release()
        return t

    def getSpeed(self):
        self.semaphore.acquire()
        s = (self.__nmea.speedunits % (self.__nmea.speed * self.__nmea.speedmultiplier))
        self.semaphore.release()
        return s
    
    def getSatellites(self):
        self.semaphore.acquire()
        s = self.__nmea.satellites
        self.semaphore.release()
        return s
    
    def getSatelliteStatistics(self):
        self.semaphore.acquire()
        ss = list(self.__nmea.ss)
        prn = list(self.__nmea.prn)
        in_view = self.__nmea.in_view
        self.semaphore.release()
        return (ss, prn, in_view)
    
    def run(self):
        print "in gps run"
        try:
            gpsdev = open('/dev/ttyS3')
        except :
            print "ERROR: GPS not connected!"
            return


        while self.running:
            line = gpsdev.readline()
            self.gpsInput(line)
	    #print self.getCoordinates()

            #print nmea.lat, nmea.lon, (nmea.speedunits % (nmea.speed * nmea.speedmultiplier))
            #print "time: %s UTC satelites: %d"%(nmea.time, nmea.satellites)
            #print nmea.ss, nmea.zs, nmea.zv
    
