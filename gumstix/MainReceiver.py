from DTN import DTNReceiveManager

import logging
logging.basicConfig()

PORT = 14000

# The next call does not return.
dtnr = DTNReceiveManager.DTNReceiveManager(PORT)

