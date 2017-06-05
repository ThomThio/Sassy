API_Server

SASSY is a wrapper for the SASSWAT API and VIYA connection. It handles initial server config and session authentication, while simplifying what you need to build out new demos or use cases.

Initial dependencies:
Python 3.5, Postman/curl/http/waitress or http sender equivalent


Library can be easily installed and run with the following:
1. pip install sassy - This will install the dependecies it needs
2. cd to your saved folder path
3. Change auth details to your respective IP, port, username and PW of your own VIYA instance. Alternatively, use your regional one by changing it in the config too. Check with your friendly IT folks if you don't know :)
4. Run main.py on a server:
		a) gunicorn --reload main:app (pip install gunicorn)
		or
		b) waitress-serve --port=8000 main:app (windows) (pip install waitress)
5. Check if its working with...
	POSTMAN
	or
	curl -v localhost:8000/things (mac/linux)
	or
	http localhost:8000/things (pip install httpie)

Done!

The ideal scenario is that any SAS Developer just needs to send a GET request to 107.14.51SasExampleNetwork:80/basicRegression
{
{Command: ‘runRegression’, params: [
“fileName”: “forecastSales,
“ddof”: 1,
“param2”: 2,
“param3”:3..
“keepSess”: true
]}
}

Getting back something like this, for possible use of data to plot, and summary statistics:
{ “data”: 
“x”:[….],
“y”:[…],
}
,{“summStats”:[
{
    “slope”: 0.51,
    “intercept”: 29,
    “resid_err”: 0.24,
    “residuals”: [….]
    “std_err”: 0.002,
    …
}

]}
}

Easy right? How about the nitty gritty code if you want to customize some functions? We want to build it like this:

from SASAPIServer import APIServer as sass

@route={‘/basicRegression’, ‘param1’,’param2’,’param3’….}
def basicRegression():
response = sass.Models.RunRegression(‘forecastSales’,ddof=1,keepSess=True,param2,param3) 	
return response
<- 
1. Tells APIServer where this function should listen to, i.e. /basicRegression end point, and the possible parameter it can receive
2. Runs a function in the Models package:
i) Asks CAS to create a new session with stored auth details
ii) Run a pre-built regression model called ‘forecastSales’, degrees of freedom 1, with additional parameters.  
iii) keepSess is True, meaning to keep the session alive, otherwise it is default to close the session
3. Returns the response in JSON format



Some technicalities:
1. HTTP request library is dependant on falcon, a python library.