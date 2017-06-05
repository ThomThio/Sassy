# things.py

# Let's get this party started!
import falcon
import Sassy
import json
import pandas as pd
from collections import defaultdict as dd 


#ensure environment is active
		# run the server 
		#Examples, with localhost and port 8000
		# gunicorn --reload main:app (pip install gunicorn)
		# OR
		# waitress-serve --port=8000 main:app (windows) (pip install waitress)
			# gunicorn: calls gunicorn to serve something
			# reload tells the server to reload the app if there is a change in any of the source files
			#main is the source file
			#app is the falcon.API

		# then run this in a separate terminal:
	# POSTMAN
	# OR
	# curl -d POST localhost:8000/things (mac/linux)
	# OR
	# http localhost:8000/things (pip install httpie)

		# What's happening:
			# 1. use curl to do a http request to locahost:8000
			#2. /things is the route you have defined in this file! Similarly, all other requests go like this, unless specifically a POST.


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status

        output = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')

        resp.body = json.dumps(output, ensure_ascii=False)

        resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages


# falcon.API instances are callable WSGI apps
app = falcon.API()
conn = Sassy.Connect()
close = Sassy.CloseSession()

# Resources are represented by long-lived class instances
things = ThingsResource()


# things will handle all requests to the '/things' URL path
app.add_route('/things', things)

app.add_route('/conn',conn)

app.add_route('/close',close)






Sassy.Connect()
Sassy.CloseSession()



# print (jsonBuilder())