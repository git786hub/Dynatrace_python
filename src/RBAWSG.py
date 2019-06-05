# AUTOSCRIPT NAME: RBAWSG
# CREATEDDATE: 2011-11-22 17:18:42
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2012-12-12 13:40:29
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.iface.mic import EndPointCache
from psdi.iface.router import Router
import sys

try:
  from com.ibm.websphere.management import AdminClient;
  from com.ibm.websphere.management import AdminClientFactory;
except:
  print "This is supported only on WebSphere. Please run this on a WebSphere server." 
  rba_rc = "1"

from javax.management import *;
from java.util import *;


worklogDesc = "RBAWSG script\n"
hostname = ipaddress

try:
  incident  = scriptHome.getString("TICKETID").strip();
  print 'Running RBAWSG for Incident = ' + incident
 
  # format the start of the worklog entry
  worklogDesc = worklogDesc + "The incident ID is: " + incident + "\n"
  worklogDesc = worklogDesc + "CI operated on: " + ipaddress + ":" + port + "\n"

  # get WAS Handler. If not specified - use the default RBA_WAS endpoint name
  if credentials is None:
    credential_to_use = "RBA_WAS"     
  else:
    credential_to_use = credentials
  handler = Router.getHandler( credential_to_use)
  print "using end point: ", credential_to_use

  # format Get Applications Running on WebSphere Application Server command
  username = handler.getUserId();
  print "username", username
  
  endPointInfo = EndPointCache.getInstance().getEndPointInfo(credential_to_use)
  password  = endPointInfo.getProperty("PASSWORD").getValue()
 
  print "hostname = ", hostname
  
  props = Properties();
  props.setProperty( AdminClient.CONNECTOR_TYPE, AdminClient.CONNECTOR_TYPE_SOAP );
  props.setProperty( AdminClient.CONNECTOR_HOST, hostname );
  props.setProperty( AdminClient.CONNECTOR_PORT, port );
  props.setProperty( AdminClient.USERNAME, username );
  props.setProperty( AdminClient.PASSWORD, password );
  client = AdminClientFactory.createAdminClient(props);
  
  query = "*:type=J2EEApplication,*";
  queryName = ObjectName(query);
  print "query name", queryName
  apps = client.queryNames( queryName, None);
  
  i = apps.iterator();
  while i.hasNext():
    app = i.next();
    name = client.getAttribute( app, "objectName" );
    state = client.getAttribute( app, "state" );
    if state == 1:
      statename = "running";
    elif state == 3:
      statename = "stopped";
    else:
      statename = state;
    print "[" + name + "], State="+statename;  
    worklogDesc = worklogDesc + "[" + name + "]\n[State:" + statename + "]\n\n"
  rba_rc = "0"
  
except:
  print "Catch All: Exception occurred in running this script: ", sys.exc_info()
  worklogDesc = worklogDesc + "Error in running the script - please check the credentials specified in the End Point: " + credential_to_use + "\n"
  worklogDesc = worklogDesc + "Please look at the action log for more information"
  rba_rc = "5"

try:
  # Record the output in a new worklog entry
  worklogSet = scriptHome.getMboSet("MODIFYWORKLOG")
  worklogMbo = worklogSet.add()
  worklogMbo.setValue("description", "RBAWSG Results")
  worklogMbo.setValue("description_longdescription", worklogDesc)

 
except:
  print "Error writing to results windows: ", sys.exc_info()
  rba_rc = "6"

print 'Script RBAWSG completed'