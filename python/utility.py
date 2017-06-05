from collections import defaultdict

def headers_toReadable(rawText):
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
				d[last] = t

	return d



def casOutput_toReadable(rawText):

	if type(rawText) is not str:
		rawText = rawText.__dict__
		return rawText
		
	d = defaultdict()

	last = ""


	rawText = rawText.split("\n")
	print(rawText)
	# for t in rawText:


	return d