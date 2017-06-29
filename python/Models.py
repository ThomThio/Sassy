#!/usr/bin/env python
#title           :Sassy.py
#description     :Modelling layer and controller
#author          :Thomas Thio
#date            :20170608
#version         :1.4
#usage           :Called in response to POST param 'Model' 
#notes           :
#python_version  :3.6.0  
#==============================================================================

import utility
import json
from collections import defaultdict
import pandas as pd
from itertools import chain
import traceback
import sys

#pass in a connection object to the function. This is provide flexibility in how you want to interact with CAS as virtually anything in the scope of CAS can be done with the connection object.
#For this sample purpose, it shows the most generic way to upload external data to CAS, get a dataframe object, perform CAS Actions on it and return the respective output you want.
#Reason is to abstract the Sassy class (purely restful api controller) and the Models class (almost-purely for models/use case scenarios)
def TemplateModel(conn, argDict):
	link = "www.sas.com.sg"
	msg = "Template model successfully executed!"
	dFrame = None


	### MODEL LOGIC HERE ###

	modelOutput = defaultdict()
	modelOutput['link'] = link
	modelOutput['msg'] = msg
	modelOutput['dFrame'] = dFrame

	# modelOutput = {**modelOutput,**argDict} #python 3.5 only
	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7
	return modelOutput

def SampleModel(conn, argDict):

	#do something with the connection
	#1. Load data
	#2. Run simple correlation matrix op
	#3. Output the results
	Web_data_link = argDict['Web_data_link']
	casOut = conn.upload(Web_data_link)
	link = None
	msg = "Sample model ran!"
	dFrame = None
 
 
	irisTbl = casOut.casTable #casTable borrows alot from the pandas dataframe! Be wary of overrides. Basic calls are similar though (please check the latest documentation on VIYA/CasTable for detailed information as each version varies)

	#use the connection to execute actions on CAS Tables
	#Example, Pearson correlation to generate product-moment correlation coef
	corrOutput = conn.simple.correlation(irisTbl)


	#ensure modeloutput is turned into json first, in whichever data structure format you wish.
	
	#if your output is a castable/dataframe, no problem. pandas has additional params to state how it will transform the dataframe into the json format/structure you want
	#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html
	#e.g. modelOutput = tbl.to_json() 
	#if your output of the model is a CASResult, this has to be handled differently! In this example, we will output a
	#NOTE: CasResult does not have a fixed formatting at time of this writing, you may see alot of spaces and \n - i.e. you need to clean it up after calling it

	corrOutput = str(corrOutput)
	corrOutput = json.dumps(corrOutput)
	corrOutput, msg = utility.casOutput_toReadable(corrOutput)
	
	modelOutput = defaultdict()
	modelOutput['pearson_correlation'] = corrOutput
	modelOutput['link'] = link
	modelOutput['msg'] = msg
	modelOutput['dFrame'] = dFrame
	
	# modelOutput = {**modelOutput,**argDict}
	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7
	return modelOutput

 
def RunSampleNN(conn, argDict):
	link = '/Users/sasdemo01/My Folder/Iris_NN_report' #can this give the results, or is merely a web link to access and display? If so we can send a redirect to the VI/VA report in the future
  
	link = '/reports/reports/fec677db-3abf-4175-9e91-10d5da08d96f'
  
	#e.g. http://172.27.217.62/links/resources/report/?uri=/reports/reports/6c2b3c1c-d598-4f8f-ac0c-f84e59978093&page=vi931 
	msg = "Neural network sample ran!"
	dFrame = None

	modelOutput = defaultdict()
	modelOutput['link'] = link
	modelOutput['msg'] = msg
	modelOutput['dFrame'] = dFrame
	# modelOutput['Alexa_speech'] = 


	# modelOutput = {**modelOutput,**argDict}
	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7
	return modelOutput


def RunTSForecast(conn, argDict):

	SASCode = "libname myloclib '/opt/sasinside/DemoData/';\
				libname mycaslib cas caslib=casuser;\
%%if not %%sysfunc(exist(mycaslib.pricedata)) %then %%do; \
 data mycaslib.pricedata;\
	set myloclib.pricedata;\
  run;\
%%end;\
proc tsmodel data   = mycaslib.pricedata\
			 outobj = (\
					   outFor  = mycaslib.outFor /* output object tied to the outfor table in the caslib*/\
					   outEst  = mycaslib.outEst\
					   outStat = mycaslib.outStat\
					   );\
	by regionname productline productname;\
	id date interval=month;\
	var sale /acc = sum;\
	var price/acc = avg;\
	require atsm;\
	submit;\
		declare object dataFrame(tsdf);\
		declare object my_diag(diagnose);\
		declare object my_diagSpec(diagspec);\
		declare object forecast(foreng);\
		declare object outFor(outfor);\
		declare object outEst(outest);\
		declare object outStat(outstat);\
		rc = dataFrame.initialize();\
		rc = dataFrame.addY(sale);\
		rc = dataFrame.addX(price);\
		rc = my_diagSpec.open();\
		rc = my_diagSpec.setArimax('identify', 'both');\
		rc = my_diagSpec.setEsm('method', 'best');\
		rc = my_diagSpec.close();\
		rc = my_diag.initialize(dataFrame);\
		rc = my_diag.setSpec(my_diagSpec);\
		rc = my_diag.run();\
		rc = forecast.initialize(my_diag);\
		rc = forecast.setOption('lead', 12, 'holdoutpct', 0.1);\
		rc = forecast.run();\
		rc = outFor.collect(forecast);\
		rc = outEst.collect(forecast);\
		rc = outStat.collect(forecast);\
  endsubmit;\
run;\
"
	runCode_out = conn.dataStep.runCode(code=SASCode)

	print("Run code output")
	print(runCode_out)

	modelOutput = defaultdict()
	modelOutput['link'] = link
	modelOutput['msg'] = msg
	modelOutput['dFrame'] = runCode_out
	# modelOutput = {**modelOutput,**argDict}
	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7

	return modelOutput

  
  
def RunLoans(conn, argDict):
  
  #if profile does not exist, add it to the loan dataset/DB *recommend DB as flatfile dataset may be used by other sessions!
	
  #run risk assessment based on model
  
  #output result
  
	link = None
	msg = "Loan Models run!"
	dFrame = None

	profile = argDict['Profile']


	sess = conn
	indata_dir="../../data"
	indata="bank"

	sess.loadactionset(actionset="table")
	sess.loadactionset(actionset="sampling")
	sess.loadactionset(actionset="regression")
	sess.loadactionset(actionset="percentile")

	if not sess.table.tableExists(table=indata).exists:
		tbl = sess.upload_file(indata_dir+"/"+indata+".sas7bdat", casout={"name":indata})

	sess.sampling.stratified(
	  table={"name":"bank"},
	  output={"casOut":{"name":"bank_part", "replace":True}, "copyVars":"ALL"},
	  samppct=70,
	  partind=True
	)

	gm = sess.regression.genmod(
	  table={"name":"bank_part"},
	  classVars=[{"vars":{"cat_input1", "cat_input2"}}],
	  model={
		"depvars":[{"name": "int_tgt"}],
		"effects":[{"vars":{"cat_input1", "cat_input2", "logi_rfm1", "logi_rfm2", "logi_rfm3", "logi_rfm4",
						   "logi_rfm5", "logi_rfm6", "logi_rfm7", "logi_rfm8", "logi_rfm9", "logi_rfm10", 
							"logi_rfm11", "logi_rfm12"}}],
		"dist":"NEGBIN",
		"link":"LOG"
	  },
	  selection={"method":"FORWARD", "choose":"SBC", "select":"SBC", "stop":"SBC"},
	  partByVar={"name":"_partind_", "train":"1", "validate":"0"},
	  output={
		"casOut":{"name":"_scored_glm", "replace":True}, 
		"copyVars":"ALL",
		"resRaw": "Residual",
		"pred":"Prediction",
		"h" : "Leverage"
	  }
	)

	# Output model statistics
	df = sess.CASTable("_scored_glm")
	df = df[df._PartInd_ == 0][df.Residual.notnull()].to_frame()
	print(df.head())




	modelOutput = defaultdict()
	modelOutput['link'] = link
	modelOutput['msg'] = msg
	modelOutput['dFrame'] = df






	# modelOutput = {**modelOutput,**argDict}
	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7
	return modelOutput


def SampleHyperGroup(conn,argDict):
	link = None
	msg = "Sample Hypergroup ran!"
	dFrame = None

	#1. loadTable: caslib='TEMP', path='NETWORK_DATASET.sashdat'
	#print("Table loaded")
	# loadedTable = conn.read_csv("../data/network_dataset.csv")

	# loadedTable = conn.load('NETWORK_DATASET' ,caslib='public')
	# print(loadedTable.head(3))
	tableName = "NETWORK_DATASET"
	tableLib = "public"
	# tableName = loadedTable.name 
	# tableLib = loadedTable.caslib

	#2. loadActionSet: actionSet='hyperGroup'
	as_info = conn.loadactionset('hyperGroup')

	print("Action loaded")

	#3. run CAS action: act='runCode' (API: runCode)
	runCode_out = conn.dataStep.runCode(code=\
	"data NETWORK; \
	set " + tableLib+"."+ tableName + ";\
	 SOURCE = put(FROM,best.);\
	 TARGET = put(TO,best.);\
	run;")

	print(" NETWORK Table loaded")

	# 4.Use HyperGroup action to populate EDGES and NODES table.
	hypGrp_out = conn.hyperGroup.hypergroup(
		allGraphs=True,
		centrality=True,
		community=True,
		createOut="NEVER",
		edges={"name":"EDGES","replace":True},
		inputs=["SOURCE","TARGET"],
		nCommunities="5",
		scaleCentralities="CENTRAL1",
		table="NETWORK",
		vertices={"name":"NODES","replace":True}
	)

	print("Hypergroup output")
	# print(hypGrp_out)

	#5. fetch result
	filterCommunity = -1
	nodes = conn.CASTable('nodes')
	if filterCommunity >= 0:
		nodes.where = "_Community_ EQ %F" % filterCommunity
	nodesOut = conn.fetch(nodes, fetchVars=['_Value_','_Community_','_CentroidAngle_'],to=1000,sastypes=False, format=True)
	# nodesOut = conn.fetch(nodes,to=300,sastypes=False, format=True)
	nodes = nodesOut['Fetch']
	# nodes.reset_index()
	# nodes.reindex(index=range(len(nodes)))
	# print(nodes.index)
	# print(nodes.head(3))
	# print(nodes.columns)
	nodes_json = nodes.to_json(orient='table')
	edges = conn.CASTable('edges')
	if filterCommunity >= 0:
		edges.where = "_SCommunity_ EQ %F AND _TCommunity_ EQ %F" % (filterCommunity,filterCommunity)
	edgesOut = conn.fetch(edges, fetchVars=['_Source_','_Target_','_TargetCentAngle_'],to=1000,sastypes=False, format=True)
	# edgesOut = conn.fetch(edges,to=300,sastypes=False, format=True)
	edges = edgesOut['Fetch']
	# edges.reset_index()
	# edges.reindex(index=range(len(edges)))
	# print(edges.head(3))
	# print(edges.columns)
	edges_json = edges.to_json(orient='table')
	
	# print(edges)

	# Such that JS can interpret in this format:
	# var x 	= api.results;
	# var y 	= x[Object.keys(x)[0]];
	modelOutput = defaultdict()
	modelOutput['link'] = link
	modelOutput['msg'] = msg


	# {{'title':'nodes'},{'schema':nodes.columns},{'rows':nodes.as_matrix()}}
	temp_dict = defaultdict()
	temp_dict['title'] = 'nodes'
	nodes.reset_index(inplace=True)
	temp_dict['schema'] = nodes.columns.tolist()
	temp_dict['rows'] = nodes.as_matrix().tolist()

	nodes_dict = defaultdict()
	nodes_dict['nodes'] = temp_dict

	modelOutput['nodes_results'] = nodes_dict

	temp_dict = defaultdict()
	temp_dict['title'] = 'edges'
	edges.reset_index(inplace=True)
	temp_dict['schema'] = edges.columns.tolist()
	temp_dict['rows'] = edges.as_matrix().tolist()

	edges_dict = defaultdict()
	edges_dict['edges'] = temp_dict

	modelOutput['edges_results'] = edges_dict
	# modelOutput['dFrame'] = {"nodes":nodes,"edges":edges}
	# modelOutput['conn_func'] = str(conn.__dict__)

	# modelOutput = {**modelOutput,**argDict}


	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7

	return modelOutput


def Y3Demo(conn, argDict):
	link = 'http://172.27.217.62/links/resources/report/?uri=/reports/reports/6c2b3c1c-d598-4f8f-ac0c-f84e59978093&page=vi931'
	msg = "OK"
	dFrame = None


	print(argDict)

	modelOutput = defaultdict()
	modelOutput['link'] = link
	modelOutput['msg'] = msg
	modelOutput['dFrame'] = None
	# modelOutput = {**modelOutput,**argDict}
	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7

	return modelOutput


def WaterConsumeDemo(conn,argDict):

	link = 'http://172.27.217.62/reports/reports/071f6101-d9b3-4d69-a2a5-731a10d030c7'
	msg = "OK"
	dFrame = None

	modelOutput = defaultdict()
	modelOutput['link'] = link
	modelOutput['msg'] = msg
	modelOutput['dFrame'] = None
	# modelOutput = {**modelOutput,**argDict}
	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7

	return modelOutput



def LogisticsNetworkAnalysis(conn, argDict):
	link = "www.sas.com.sg"
	msg = "Logistics network model successfully executed!"
	dFrame = None


	### MODEL LOGIC HERE ###

	#load data
	mainDataFile = "c2k_data.xlsx"
	attributesFile = "c2k_attributes.xlsx"

	loadedTable = conn.upload("../data/LogisticsNetworkData/" + mainDataFile)
	print(loadedTable.head(3))
	tableName = loadedTable.name 

	attributeTable = conn.upload("../data/LogisticsNetworkData/" + attributesFile)

	print(attributeTable.head(3))
	attr_tableName = attributeTable.name 



	modelOutput = defaultdict()
	modelOutput['link'] = link
	modelOutput['msg'] = msg
	modelOutput['dFrame'] = dFrame

	# modelOutput = {**modelOutput,**argDict} #python 3.5 only
	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7
	return modelOutput


def FactMac(conn, argDict):
	link = argDict['link']
	msg = "Factorization machine ran!"
	dFrame = None


	### MODEL LOGIC HERE ###

	modelOutput = defaultdict()
	modelOutput['link'] = link
	modelOutput['msg'] = msg
	modelOutput['dFrame'] = dFrame

	# modelOutput = {**modelOutput,**argDict} #python 3.5 only
	modelOutput = dict(chain.from_iterable(d.iteritems() for d in (modelOutput, argDict))) #python 2.7
	return modelOutput

def FormError(errMsg):
	d = defaultdict()
	d['msg'] = errMsg
	return d


def ModelControl(conn, argDict, **kwargs):
	mdl = argDict['Model']

	try:
		if mdl == "HyperGroup":
			return SampleHyperGroup(conn,argDict)
		elif mdl == "SampleModel":
			return SampleModel(conn,argDict)
		elif mdl == "RunLoans":
			return RunLoans(conn,argDict)
		elif mdl == "RunTSForecast":
			return RunTSForecast(conn,argDict)
		elif mdl == "RunSampleNN":
			return RunSampleNN(conn, argDict)
		elif mdl == "Y3Demo":
			return Y3Demo(conn,argDict)
		elif mdl == "WaterConsumeDemo":
			return WaterConsumeDemo(conn, argDict)
		elif mdl == "LogisticsNetworkAnalysis":
			return LogisticsNetworkAnalysis(conn, argDict)
		elif mdl == "FactMac":
			return FactMac(conn,argDict)
		else:
			return FormError("Model not recognized. Are parameters correctly stated; has it been built yet?")
	except Exception as e:
		traceback.print_exc()
		return FormError("An error occured, model did not run fully. Are parameters correctly stated; has it been built yet? \n Error:" + str(e))