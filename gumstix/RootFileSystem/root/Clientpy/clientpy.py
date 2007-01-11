#!/usr/bin/python

import socket
import pickle
import time
import threading

class ConnectionThread ( threading.Thread ):

	def run ( self ):
		client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
		client.connect ( ("localhost", 7915) )


#		print pickle.load ( client.recv ( 1024 ) )
		while ( 1 ):
			print client.recv(1024)


		client.close()


ConnectionThread().start()

