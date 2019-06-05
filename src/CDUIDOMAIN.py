# AUTOSCRIPT NAME: CDUIDOMAIN
# CREATEDDATE: 2015-08-16 13:58:55
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2015-08-16 09:55:48
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.server import MXServer
from java.util import HashMap

#Set the json answer as body type
responseHeaders.put("content-type","application/json")
set = MXServer.getMXServer().getMboSet("CDUITABLEDOMAIN",request.getUserInfo())
cr = set.add()
responseBody = cr.evaluateDomain(requestBody)
set.deleteAll()