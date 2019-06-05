# AUTOSCRIPT NAME: RBAWASSTP
# CREATEDDATE: 2011-08-26 15:00:00
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2012-12-12 13:40:02
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.iface.mic import EndPointCache
from psdi.iface.router import Router
from com.ibm.ism.rba.app.utils import RBAUtils
import sys
from com.ibm.websphere.management import AdminClient;
from com.ibm.websphere.management import AdminClientFactory;
from javax.management import *;
from java.util import *;

worklogDesc = "RBAWASSTP script\n"
hostname = ""
try:
  workorder = scriptHome.getString("WONUM").strip();
  print 'Running RBAWASSTP for WorkOrder = ' + workorder
  print 'scriptHome = ', scriptHome
  iparray = RBAUtils.getStringArray("ci_address")
  hostname = iparray[0]
  portarray = RBAUtils.getStringArray("ci_port")
  port = portarray[0]
  appname = RBAUtils.getString("ci_appname")
  print "CI in Work Order: [Host] ", hostname
  print "CI in Work Order: [Port] ", port
  print "CI in Work Order: [App] ", appname
  
  # format the start of the worklog entry
  worklogDesc = worklogDesc + "RBAWASSTP script run for Work Order: " + workorder + "\n"
  worklogDesc = worklogDesc + "CI operated on: " + hostname + ":" + port + "\n"
  
  # get SSHWO Handler
  handler = Router.getHandler( "SSHWO" )
  
  # format Stop application running on a WebSphere Application Server command
  username = handler.getUserId();  
  print "username", username
  
  endPointInfo = EndPointCache.getInstance().getEndPointInfo("SSHWO")
  password  = endPointInfo.getProperty("PASSWORD").getValue()

  props = Properties();
  props.setProperty( AdminClient.CONNECTOR_TYPE, AdminClient.CONNECTOR_TYPE_SOAP );
  props.setProperty( AdminClient.CONNECTOR_HOST, hostname );
  props.setProperty( AdminClient.CONNECTOR_PORT, port );
  props.setProperty( AdminClient.USERNAME, username );
  props.setProperty( AdminClient.PASSWORD, password );
  client = AdminClientFactory.createAdminClient(props);
  
  query = "*:type=J2EEApplication,name=" + appname + ",*";
  queryName = ObjectName(query);
  print "query name", queryName
  apps = client.queryNames( queryName, None);
  if apps.isEmpty():
    print "3"
    print "Application " + appname + " not found.";
    worklogDesc = worklogDesc + "Application " + appname + " not found " + "\n"
  else:
    app = apps.iterator().next();
  
  state = client.getAttribute( app, "state" );
  print "state", state
  if state == 3:
    print "Application " + appname + " on " + hostname + " already stopped";
    worklogDesc = worklogDesc + "Application " + appname + " on " + hostname + " already stopped" + "\n"
  elif state == 1:
    try:
      client.invoke(app, "stop", [], [] );
    except:
      print "Catch All: Exception occurred in stoppping the WebSphere Application Server: ", sys.exc_info()
      worklogDesc = worklogDesc + "Error stopping WebSphere Application Server - please check server " + hostname + " credentials defined by SSHWO End Point"
      rc = "4"
    print "Application " + appname + " on " + hostname + " stopped";
    worklogDesc = worklogDesc + "Application " + appname + " on " + hostname + "  stopped" + "\n"
  rc = "0"
except:
  print "Catch All: Exception occurred in running this script: ", sys.exc_info()
  worklogDesc = worklogDesc + "Error stopping WebSphere Application Server - please check server " + hostname + " credentials defined by SSHWO End Point"
  rc = "5"

try:
  # Record the output in a new worklog entry
  worklogSet = scriptHome.getMboSet("MODIFYWORKLOG")
  worklogMbo = worklogSet.add()
  worklogMbo.setValue("description", "RBAWASSTP Results")
  worklogMbo.setValue("description_longdescription", worklogDesc)

  # set the rc in the workorder
  print "RC =", rc
  RBAUtils.put("rba_rc", rc)

except:
  print "Error writing to results windows: ", sys.exc_info()
  rc = "6"

print 'Script RBAWASSTP completed'