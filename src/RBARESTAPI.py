# AUTOSCRIPT NAME: RBARESTAPI
# CREATEDDATE: 2011-11-11 11:38:10
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2012-12-11 17:22:48
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

'''
This script provides an example on how to invoke a rest API call from within an ITUSC automation script.

The overall purpose of this script is to retrieve a list of all of the windows computer system
CI names from the ITUSC server.

This script utilizes the built in endpoint MBO object in ITUSC to isolate credentials from the
end user that executes this script. That is, the end user that executes this script will never
see or enter the password for the target machine.

This script additionally shows how to send a REST api call to ITUSC to retrieve data, and how to use
the JSON object to parse the results.

This script assumes that one attribute/property is passed in: 

credentials - This attribute should contain the name of the endpoint mbo defined that contains
the credentials of the server that the REST call will be made against. This enpoint mbo will
have not only the URL of the server, but the username and password.


'''

# The Router object is used to retrieve the endpoint point object/handler
from psdi.iface.router import Router
from psdi.iface.mic import EndPointCache
from java.lang import String
from com.ibm.json.java import JSONObject
import sys

worklogDesc = ""
try:

  # get Endpoint/Handler. If not specified - use the default RBA_REST endpoint name
  if credentials is None:
    credential_to_use = "RBA_REST"     
  else:
    credential_to_use = credentials
  print "using end point: ", credential_to_use

  handler = Router.getHandler(credential_to_use)

  print "credentials being used: ", credential_to_use
  # get the username, password and url from the endpoint mbo
  username = handler.getUserName();
  print "username = ", username
  
  endPointInfo = EndPointCache.getInstance().getEndPointInfo(credential_to_use)
  password  = endPointInfo.getProperty("PASSWORD").getValue()
  
  url = handler.getUrl()
  print "url =", url
 
  # This script requires two different calls to properly retrieve the information.
  #
  # Since the CI objects only contain the id of the classification that defines their
  # type, we need to find that id first. So we will query the classstructure object
  # and ask for it.
  #
  # we need to get the classstructureid of the CI.WINDOWSCOMPUTERSYSTEM
  # our URL should be appended with the following:   classstructure
  newUrl = url + "classstructure"
  
  # See the REST api documentation for a full run down on the query format. This query is saying:
  #
  # _format=json <== Return the data as a json object, if this isn't in the query xml will be returned.
  # _compact=1 <== Return the minimal amount of text
  # _includecols=classstructureid <= Only return this column data
  # classificationid=~eq~CI.WINDOWSCOMPUTERSYSTEM <= The classificationid column MUST match CI.WINDOWSCOMPUTERSYSTEM
  query = "_format=json&_compact=1&_includecols=classstructureid&classificationid=~eq~CI.WINDOWSCOMPUTERSYSTEM"
  paramMap = {"URL":newUrl, "username":username, "password":password}
  # The handler.invoke returns a byte[], so we use the Java String object to convert it for us.
  result = String(handler.invoke(paramMap, query))
  
  # We printed the json here to see what the format was to properly dig into the resultant object.
  # print "Got back: ", result
  jsn = JSONObject.parse(result)
  
  # The format of this was an outer 'set' object, that had an object of type CLASSSTRUCTURE which contained
  # an array of CLASSSTRUCTURES. We knew it would return only one, so we get the first. Since we only
  # asked for the CLASSSTRUCTUREID field, we just retrieved that.
  #
  # FYI - The JSONObject is just an object that extends a java hashmap and adds a parser.
  resultSet = jsn.get("CLASSSTRUCTUREMboSet")
  cs = resultSet.get("CLASSSTRUCTURE")
  csid = cs.get(0).get("CLASSSTRUCTUREID")

  # Now reformat and get the windows computersystems
  # now change the url and append ci
  newUrl = url + "ci"
  query = "_format=json&_compact=1&_includecols=ciname&classstructureid=~eq~" + csid
  paramMap = {"URL":newUrl, "username":username, "password":password}
  result = String(handler.invoke(paramMap, query))

  # Print the result string
  print "Got result: ", result
  worklogDesc = worklogDesc + "Current set of Windows computer systems:\n\n"
  jsn = JSONObject.parse(result)
  resultSet = jsn.get("CIMboSet")
  cs = resultSet.get("CI")
  # here we knew we might get back more than one, so we iterate across them and
  # log the results.
  for ci in cs:
    worklogDesc = worklogDesc + ci.get("CINAME") + "\n"

  worklogDesc = worklogDesc + "\n\njson result: " + result

  # Record the output in a new worklog entry
  #
  # scriptHome is the MBO that this script is acting against. In this case
  # we are getting a related mbo set for the log, then adding a new log 
  # object, and saving our collected information.
  worklogSet = scriptHome.getMboSet("MODIFYWORKLOG")
  worklogMbo = worklogSet.add()
  worklogMbo.setValue("description", "REST API: GET WINDOWS_CS Results")
  worklogMbo.setValue("description_longdescription", worklogDesc)

  rba_rc = "0"

except:
  print "Unable to complete the REST API:", sys.exc_info()  
  worklogSet = scriptHome.getMboSet("MODIFYWORKLOG")
  worklogMbo = worklogSet.add()
  worklogMbo.setValue("description", "REST API: GET_WINDOWS_CS failed")  
  worklogDesc = worklogDesc + "Look at the action log for more details"
  worklogMbo.setValue("description_longdescription",  worklogDesc)
  rba_rc = "6"