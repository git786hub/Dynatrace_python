# AUTOSCRIPT NAME: CDUISTDOMAIN
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

objectName = request.getQueryParam("objectname")
objectID = request.getQueryParam("objectid")
attribute = request.getQueryParam("attribute")

set = MXServer.getMXServer().getMboSet("CDUITABLEDOMAIN",request.getUserInfo())
cr = set.add()

if(attribute == None):
	responseBody = cr.evaluateDomain(requestBody)
else:
	responseBody = cr.evaluateStandardDomain(objectName,objectID,attribute)

set.deleteAll()