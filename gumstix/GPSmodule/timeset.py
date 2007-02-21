#!/usr/bin/python

#busybox date -u MMDDhhmmYYYY.ss.ss

import time, os, threading
import gps
import sys

class TimeSet:
    def __init__(self):
        self.running = 1
	self.counting = 2    
    
    def UTCset(self):
	local = gps.GpsThread()
	local.start()
	print "Time Setting"
	counting = 2
	while self.running:
		tempTime = local.getTime()
		print "loop"
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
				os.popen("/bin/date -u %s%s%s%s%s.%s" % (tempDate[1],tempDate[0],tempTime[0],tempTime[1],tempDate[2],tempTime[2]))
				print "set"
				self.running=0
				local.stop()
				break

				#setting time using date
			else:
				print tempTime
		time.sleep(1)

        #we don't run aymore. stop the gps thread too
        

        
    def run(self):
        print "start Time Setting"
        self.UTCset()

if(__name__ == "__main__"):
    A = TimeSet()
    #A.run()
    A.UTCset()
                    
