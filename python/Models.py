
import json


#pass in a connection object to the function. This is provide flexibility in how you want to interact with CAS as virtually anything in the scope of CAS can be done with the connection object.
#For this sample purpose, it shows the most generic way to upload external data to CAS, get a dataframe object, perform CAS Actions on it and return the respective output you want.
#Reason is to abstract the Sassy class (purely restful api controller) and the Models class (almost-purely for models/use case scenarios)

def SampleModel(conn):

	#do something with the connection
	#1. Load data
	#2. Run simple correlation matrix op
	#3. Output the results
	link = 'https://raw.githubusercontent.com/pydata/pandas/master/pandas/tests/data/iris.csv'
	casOut = conn.upload(link)
 
 
	irisTbl = casOut.casTable #casTable borrows alot from the pandas dataframe! Be wary of overrides. Basic calls are similar though (please check the latest documentation on VIYA/CasTable for detailed information as each version varies)

	print(irisTbl.tableinfo())
	# print(irisTbl.head(3))
	# print(irisTbl.summary())

	#use the connection to execute actions on CAS Tables
	#Example, Pearson correlation to generate product-moment correlation coef
	corrOutput = conn.simple.correlation(irisTbl)


	#ensure modeloutput is turned into json first, in whichever data structure format you wish.
	

	#if your output is a castable/dataframe, no problem. pandas has additional params to state how it will transform the dataframe into the json format/structure you want
	#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html
	#e.g. modelOutput = tbl.to_json() 
	#if your output of the model is a CASResult, this has to be handled differently! In this example, we will output a
	#NOTE: CasResult does not have a fixed formatting at time of this writing, you may see alot of spaces and \n - i.e. you need to clean it up after calling it

	modelOutput = str(corrOutput)
	modelOutput = json.dumps(modelOutput)

	return modelOutput

  
  
def runSampleNN(conn):
  	refUrl = '/Users/sasdemo01/My Folder/Iris_NN_report' #can this give the results, or is merely a web link to access and display? If so we can send a redirect to the VI/VA report in the future
  
  	refURI = '/reports/reports/fec677db-3abf-4175-9e91-10d5da08d96f'
  
  	#e.g. http://172.27.217.62/links/resources/report/?uri=/reports/reports/6c2b3c1c-d598-4f8f-ac0c-f84e59978093&page=vi931 


	modelOutput = str(corrOutput)
	modelOutput = json.dumps(modelOutput)

	return modelOutput
  


  
def runLoans(profile, conn):
  
  #if profile does not exist, add it to the loan dataset/DB *recommend DB as flatfile dataset may be used by other sessions!
	
  #run risk assessment based on model
  
  #output results
  
  return ""