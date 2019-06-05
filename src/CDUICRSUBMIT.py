# AUTOSCRIPT NAME: CDUICRSUBMIT
# CREATEDDATE: 2015-06-21 13:58:55
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2015-06-24 09:55:48
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.server import MXServer
from java.util import HashMap

#Set the json answer as body type
responseHeaders.put("content-type","application/json")
set = MXServer.getMXServer().getMboSet("CDUICR",request.getUserInfo())
cr = set.add()
result = cr.submitCR(requestBody)
if(result.get("ERROR") == None):
	responseBody = result.get("JSON");
else:
	responseBody = result.get("ERROR");
set.save()