from DTN import DTNSendManager
from Modules import module
from Modules import gpsmodule
from Modules.GPS import gps
import sys

import logging
logging.basicConfig()

#SERVER = "128.97.93.10"
#SERVER = "192.168.2.2"
SERVER = sys.argv[1]
PORT = 14000

#the netcar id used to identify the data from this node
f = file("/etc/netcarinit/netcarID", 'r')
netcarID = f.read()
f.close()

########################
# initialize the modules
dtns = DTNSendManager.DTNSendManager(SERVER, PORT, netcarID)
#baseModule = module.BaseModule()

#this is a special module which handles data from the gps.
#gpsThread = gps.GPSThread('/dev/tty.HOLUXGR-231-SPPslave-1')
#gpsThread = gps.GPSThread('/dev/ttyS3')
gpsThread = gps.GPSThread(sys.argv[2])

locationLoggingModule = gpsmodule.LocationLoggingModule(gpsThread, delta=10)

###################################
# register modules with DTN Manager
#dtns.registerModule(baseModule)
dtns.registerModule(locationLoggingModule)

##########################
# start the module threads
dtns.start()
#baseModule.start()
gpsThread.start()
locationLoggingModule.start()
