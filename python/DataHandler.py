#!/usr/bin/env python
#title           :DataHandler.py
#description     :HTTP request/response layer
#author          :Thomas Thio
#date            :20170608
#version         :1.4
#usage           :gunicorn --reload -b 10.21.22.92:8888 Sassy:app
#notes           :
#python_version  :3.6.0  
#==============================================================================


import json
import traceback

def Load(conn, argDict): #option args of type, link, username, password, port, DBName
    
	#handle upload data via github link
	# link = 'https://raw.githubusercontent.com/pydata/pandas/master/pandas/tests/data/iris.csv'
	casOut = ""
	try:
		print("Load function in DataHandler received args:",argDict)
		if 'type' in argDict:
			if argDict['type'] == 'web':
				casOut = conn.upload(argDict['link'])

				#check if table already exists. return the error to user
				
			elif argDict['type'] == 'postgre':

				#load from local postgre connection
				#upload dataset (dataframe? pipe?)

				# casOut = conn.upload()
				print("uploaded dataset via postgre connection")


		else:
			return ("No dataset type given, skipping data load!")

	

	#handle upload data via postgre connection

	#handle upload data via...
	

		casOut = casOut.casTable.tableinfo()
		return casOut
	except Exception as e:
		print("Attempted to load data, but error occured. Please check loading action or DataHandler function")
		print(e)
		tb = traceback.format_exc()
		print(tb)
		return None
		
	return casOut
