#!/usr/bin/env python
#title           :utility.py
#description     :HTTP request/response layer
#author          :Thomas Thio
#date            :20170608
#version         :1.4
#usage           : import it into Sassy.py
#notes           :
#python_version  :3.6.0  
#==============================================================================


from collections import defaultdict

#makes received request headers into a nicely formatted dictionary
def headers_toReadable(rawText):
	print("Making headers machine readable")

	d = defaultdict()
	last = ""
	for t in rawText:
		# print(t)
		if "WebKit" in t:
			continue
	
		t = t.replace("\\r","")
		if 'form-data' in t:
			i = t.index('form-data')
			sub = t[i:]
			param = sub.replace("'","")
			param = param[11:]

			comma_i = param.index('"')
			param = param[comma_i + 1:-1]
			# print("param",param)
			d[param] = ""
			last = param
		else:
			if t != "" and t != "'}" and last != "":
				# print("value",t)
				#if argument is a link, remove additional backslashes
				if '://' in t:
					t = t.replace("\\","") 

				d[last] = t

	return d


#Returns a string out of the full params of CAS output (dictionary in string form), or formatting a singular string output (single string)
def casOutput_toReadable(rawText):
	print("Making cas output human and machine readable")

	if type(rawText) is not str:
		msg = "Cas output is not a string. Returning full dictionary of the CAS output"
		print(msg)
		rawText = rawText.__dict__
		return rawText, msg
		
	last = ""

	rawText = rawText.split("\n")
	print(rawText)
	# for t in rawText:


	return rawText, "OK"