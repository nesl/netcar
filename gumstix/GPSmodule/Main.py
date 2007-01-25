import gps
import time

GPS = gps.GpsThread()
GPS.start()

while 1:
    print GPS.getTime()
    time.sleep(1)
    
