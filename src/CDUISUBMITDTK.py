# AUTOSCRIPT NAME: CDUISUBMITDTK
# CREATEDDATE: 2016-02-07 13:54:28
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2016-02-07 11:26:28
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.server import MXServer
from java.util import HashMap

#Set the json answer as body type
responseHeaders.put("content-type","application/json")
set = MXServer.getMXServer().getMboSet("CDUIREQUEST",request.getUserInfo())
sprequest = set.add()
result = sprequest.submitTicket(requestBody)
responseBody = ""
if(result.get("ERROR") == None):
	responseBody = result.get("JSON");
else:
	responseBody = result.get("ERROR");
set.save()