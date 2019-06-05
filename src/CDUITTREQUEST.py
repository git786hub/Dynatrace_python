# AUTOSCRIPT NAME: CDUITTREQUEST
# CREATEDDATE: 2015-10-11 13:54:28
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2015-10-13 11:26:28
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.server import MXServer
from java.util import HashMap

#Set the json answer as body type
responseHeaders.put("content-type","application/json")
set = MXServer.getMXServer().getMboSet("CDUIREQUEST",request.getUserInfo())
cduirequest = set.add()
result = cduirequest.updateTicket(requestBody)
responseBody = ""
if(result.get("ERROR") == None):
	responseBody = result.get("JSON");
else:
	responseBody = result.get("ERROR");
set.save()