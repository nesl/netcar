#!/usr/bin/python

#busybox date -u MMDDhhmmYYYY.ss.ss

import time, os, threading
import gps

class TimeSet( threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsThread = gps.GpsThread()
        self.gpsThread.start()
        print "started gps thread"
        self.running = 1
	self.counting = 2    
    
    def UTCset(self):
	print "Time Setting"
	counting = 2
	while self.running:
		tempTime = self.gpsThread.getTime()
		if tempTime == '?':
			pass
		else:
			self.counting = self.counting -1
			if self.counting < 1:
				tempTime = tempTime.split(' ')
				tempDate = tempTime[0]
				tempTime = tempTime[1]
				tempDate = tempDate.split('/')
				tempTime = tempTime.split(':')
				os.popen("/bin/date -u %s%s%s%s%s.%s" % (tempDate[0],tempDate[1],tempTime[0],tempTime[1],tempDate[2],tempTime[2]))
				print "set"
				return
				#setting time using date
			else:
				print tempTime
		time.sleep(3)

        #we don't run aymore. stop the gps thread too
        self.gpsThread.running = 0
        

        
    def run(self):
        print "start Time Setting"
        self.UTCset()


                    
