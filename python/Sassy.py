import falcon
import json
import swat #(pip install python-swat-1.2.0-linux64.tar.gz, if cannot install from cmd/terminal, download the file and place in folder, run this again)
import os
import DataHandler
import Models
import utility
from collections import defaultdict

#configure this to your own VIYA instance!
host = "172.27.217.62"
port = 8777
uname = "sasdemo01"
pw = "Orion123"


#global connection variable
conn = None




class TestConnect(object):
    def on_post(self, req, resp):
        global conn
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        conn = swat.CAS(host,port,uname,pw,protocol='http')
        print(conn.serverStatus())
        output = ('CONNECTED')

        resp.body = json.dumps(output, ensure_ascii=False)
        resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages


class CloseSession(object):
    def on_post(self, req, resp):
        output = ""
        global conn
        if conn is None:
            output = ('Error: No live connections to close')
            resp.status = falcon.HTTP_400  # This is the default status

        else:
            conn.close()
            output = ('CAS Connection/Session Closed')
            resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages

        resp.body = json.dumps(output, ensure_ascii=False)


class Run(object):
    def on_post(self, req, resp):
        global conn
        output = ""
        if conn is None:
            output = ('Error: No live connections to run models on')
            resp.status = falcon.HTTP_400  # This is the default status
            # Connect()
            conn = swat.CAS(host,port,uname,pw,protocol='http')

        resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages
        
        #get params from request, run respective model
        
        #do something here
        
            
        modelOutput = (Models.SampleModel(conn))
        print(type(modelOutput))
        output = utility.casOutput_toReadable(modelOutput)

        resp.body = json.dumps(output, ensure_ascii=False)


class LoadData(object):
      def on_post(self, req, resp):
        output = ""
        global conn
        if conn is None:
            output = ('Error: No live connections')
            resp.status = falcon.HTTP_400  # This is the default status
            conn = swat.CAS(host,port,uname,pw,protocol='http')
        
        #do something here
        link = 'https://raw.githubusercontent.com/pydata/pandas/master/pandas/tests/data/iris.csv'
        # resp.body = req.stream.read()

        #Call data handler
        #passes in the json as a dictionary of arguments
        rawText = str(req.params).split("\\n")

        d = utility.headers_toReadable(rawText)

        print("HTTP Front received",d)
        # print(req.stream.read())
        # argDict = req.get_param_as_dict('form-data',required=True)
        # print(argDict)
        # print(req.get_param("link"))
        

        msg = DataHandler.Load(conn, d)
        msg = utility.casOutput_toReadable(msg)
        output = (str(msg))
        resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages

        resp.body = json.dumps(output, ensure_ascii=False)


class TemplateRequest(object):
      def on_post(self, req, resp):
        output = ""
        global conn
        
        if conn is None:
            output = ('Error: No live connections')
            resp.status = falcon.HTTP_400  # This is the default status
            conn = swat.CAS(host,port,uname,pw,protocol='http')
            #do something here
        resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages

        resp.body = json.dumps(output, ensure_ascii=False)


class Y3Demo(object):
      def on_post(self, req, resp):
        output = ""
        global conn
        if conn is None:
            output = ('Error: No live connections')
            resp.status = falcon.HTTP_400  # This is the default status
            conn = swat.CAS(host,port,uname,pw,protocol='http')
            
        output = 'http://172.27.217.62/links/resources/report/?uri=/reports/reports/6c2b3c1c-d598-4f8f-ac0c-f84e59978093&page=vi931'
            #do something here
        d = defaultdict()
        d['link'] = output
        resp.status = falcon.HTTP_200 #status can be overriden for custom error/status messages

        resp.body = json.dumps(d, ensure_ascii=False)



app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True


app.add_route('/testconn',TestConnect())
app.add_route('/load',LoadData()) #requires arguments to be specified here
app.add_route('/run',Run())
app.add_route('/run/Y3Demo',Y3Demo()) #temporary until able to arg dict through POST
app.add_route('/close',CloseSession())