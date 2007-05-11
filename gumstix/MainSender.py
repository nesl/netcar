from DTN import DTNSendManager
from Modules import module
from Modules import locationloggingmodule
from Modules.GPS import gps

import logging
logging.basicConfig()

SERVER = "suisse"
PORT = 14000

########################
# initialize the modules
dtns = DTNSendManager.DTNSendManager(SERVER, PORT)
baseModule = module.BaseModule()

#this is a special module which handles data from the gps.
gpsThread = gps.GPSThread('/dev/ttyS3')

locationLoggingModule = locationloggingmodule.LocationLoggingModule(gps)

###################################
# register modules with DTN Manager
dtns.registerModule(baseModule)
dtns.registerModule(locationLoggingModule)

##########################
# start the module threads
dtns.start()
baseModule.start()
gpsThread.start()
locationLoggingModule.start()
