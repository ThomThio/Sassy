#!/usr/bin/env python
#title           :Sassy.py
#description     :HTTP request/response layer
#author          :Thomas Thio
#date            :20170608
#version         :1.4
#usage           :gunicorn --reload -b 10.21.22.92:8888 Sassy:app
#notes           :
#python_version  :3.6.0  
#==============================================================================


import falcon
import json
import swat #(pip install python-swat-1.2.0-linux64.tar.gz, if cannot install from cmd/terminal, download the file and place in folder, run this again)
import os
import DataHandler
import Models
import traceback
import utility
from collections import defaultdict
import ast
from falcon_cors import CORS

serverType = ""

#configure this to your own VIYA instance!
host = "172.27.217.62" #ideally this should be the same server as where you are hosting the API server, makes your life much easier
port = 8777 #port of CAS
uname = "sasdemo06"
pw = "Orion123"


#global connection variable
# conn = None


if serverType == "RACE":
	host = "10.38.17.240"
	uname = "sasdemo"



class TestConnect(object):
	def on_post(self, req, resp):
		print("Test connect function entered")	
		try:
			print("Test connect on_POST entered")
			# global conn
			"""Handles GET requests"""
			resp.status = falcon.HTTP_200  # This is the default status
			conn = swat.CAS(host,port,uname,pw,protocol='http')
			print(conn.serverStatus())
			output = ('CONNECTED')

			resp.body = json.dumps(output, ensure_ascii=False)
			resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages
		except Exception as e:
			print(e)
			traceback.print_exc()
			resp.body = ("Exception caught"+e)
			resp.status = falcon.HTTP_400
			print("Exception caught!")
		finally:
			print("go to finally")
			traceback.print_exc()
			# resp.body = ("Finally ran")
			# resp.status = falcon.HTTP_400
			conn.close()


class CloseSession(object):
	def on_post(self, req, resp):
		output = ""
		# global conn
		output = ('Error: No live connections to close')
		resp.status = falcon.HTTP_400  # This is the default status
		output = ('CAS Connection/Session Closed')
		resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages

		resp.body = json.dumps(output, ensure_ascii=False)


class Run(object):
	def on_post(self, req, resp):
		try:
			# global conn
			output = ""
			output = ('Error: No live connections to run models on')
			resp.status = falcon.HTTP_400  # This is the default status
			# Connect()
			conn = swat.CAS(host,port,uname,pw,protocol='http')


			print("received params to run model",req.params)
			rawText = str(req.params).split("\\n")

			d = utility.headers_toReadable(rawText)
			if any(d) is False:
				# d = ast.literal_eval(req.params)
				d = req.params
				print("Converted string literal to dict",d)

			
			#ModelControl get params from request, run respective model
			modelOutput = (Models.ModelControl(conn, d))
			print("Run complete")
			
			resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages
			resp.body = json.dumps(modelOutput, ensure_ascii=False)
		except Exception as e:
			print(e)
			traceback.print_exc()
			resp.body = (e)
		finally:
			conn.close()


class LoadData(object):
	  def on_post(self, req, resp):
		try:
			output = ""
			# global conn
			output = ('Error: No live connections')
			resp.status = falcon.HTTP_400  # This is the default status
			conn = swat.CAS(host,port,uname,pw,protocol='http')
			
			#Call data handler
			#passes in the json as a dictionary of arguments
			rawText = str(req.params).split("\\n")

			d = utility.headers_toReadable(rawText)

			print("HTTP Front received",d)

			msg = DataHandler.Load(conn, d)
			msg = utility.casOutput_toReadable(msg)
			output = (str(msg))
			resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages

			resp.body = json.dumps(output, ensure_ascii=False)
		finally:
			conn.close()


class TemplateRequest(object):
	
	  def on_post(self, req, resp):
		try:
			output = ""
			# global conn
			
			output = ('Error: No live connections')
			resp.status = falcon.HTTP_400  # This is the default status
			conn = swat.CAS(host,port,uname,pw,protocol='http')
				#do something here
			resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages

			resp.body = json.dumps(output, ensure_ascii=False)
		finally:
			conn.close() #remember to close the session!


cors = CORS(allow_all_origins=True,allow_all_headers=True)
app = falcon.API(middleware=[cors.middleware])
# app = falcon.API()
# print("This runs")

#app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True


app.add_route('/testconn',TestConnect())
app.add_route('/load',LoadData()) #requires arguments to be specified here
app.add_route('/run',Run()) #pass in args of Model, Profile
app.add_route('/close',CloseSession())