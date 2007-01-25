import gps
import time

gps.GpsThread().start()

while 1:
    print gps.GpsThread().getTime()
    time.sleep(1)
    
