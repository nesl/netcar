from DTN import DTNReceiveManager
from Modules import gpsmodule

import logging
logging.basicConfig()

PORT = 14000

dtnr = DTNReceiveManager.DTNReceiveManager(PORT)
locationDecodingModule = gpsmodule.LocationDecodingModule()

################################
# register modules
dtnr.registerModule(locationDecodingModule)
    
################################
# The next call does not return.
dtnr.start()
