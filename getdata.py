import pandas as pd
import pymapd
import os
import datetime
import time
import pytz


mapdhost = 'use2-api.omnisci.cloud'
mapdport = '443'
mapduser = 'X27373D8205D04EF6AE5'
mapdpass = 'fm5KfyCfq3hWI96ghWkPHwDZg5MmSwt4FKo8P41a'
mapddbname = 'mapd'
mapdprotocol = 'https'
def tweets():
	#print('Connecting to MapD server {0} on port {1} using {2} protocol'.format(mapdhost,mapdport,mapdprotocol))
	mapdcon = pymapd.connect(user=mapduser, password=mapdpass, host=mapdhost, dbname=mapddbname, port=mapdport, protocol=mapdprotocol)
	# Make sure that the connection went through
	#print(mapdcon)
	# Example SQL query where we are extracting the MOVEMENT_ID from the san_francisco_taz table for a certain location defined by latitude/
	query  = "SELECT column_1, column_2  FROM budget_tips9876"
	#print(query)
	df = mapdcon.execute(query)
	#print(df.rowcount) # count of rows returned
	#print(list(df)) # the result is returned as a python list
	
	return tweets


"""if __name__ == '__main__':
   main()"""
