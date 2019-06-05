# AUTOSCRIPT NAME: RBAGETCIIP
# CREATEDDATE: 2011-11-22 11:25:19
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2011-11-28 16:37:12
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

'''
This script provides an example on how to traverse a set of CI mbos from a starting point in search
of an object. Be forewarned that this code leverages knowledge of the Common Data Model to look
for specific relations and MBOs to reach its goal.

This script will leverage a new object type in ITUSC called a classification group. An assumption will
be made about the id(s) of certain classification groups in order to properly identify the CI type
that is being used as a starting point.

In general the main relationships we are looking for are:

Computersystem->contains->IPInterface
IPInterface->bindsTo->IPV4Address

As a corrallary we will also support Database, ApplicationServer, WebServer types. 

database->runson->computersystem
applicationserver->runson->computersystem
webserver->runson->computersystem

Assumed input/output variables supplied by the script engine in ITUSC:

input:
None - Since this example is based on an incident, the incident already
has a relationship to the ci, so we will use that relationship VIEWACTCI

output:
ipaddress <= The spec attribute where the ipaddress discovered will be placed.

'''
from psdi.mbo import MboRemote, MboSetRemote

import sys

def findFromCS(csCi):
    print "finding Ip using computersystem"
    interfaceRelSet = csCi.getMboSet("CCI_SCI_CIRELATION_CSTOIPINT")
    if interfaceRelSet.isEmpty():
        return
    for i in xrange(interfaceRelSet.count()):
      ipIntRel = interfaceRelSet.getMbo(i)
      ipInt = ipIntRel.getMboSet("TARGETCI").getMbo(0)
      ipAddrRelSet = ipInt.getMboSet("CCI_SCI_CIRELATION_IPINTTOIP");
      if ipAddrRelSet.isEmpty():
        return
      for j in xrange(ipAddrRelSet.count()):
        ipAddrRel = ipAddrRelSet.getMbo(j)
        ipAddr = ipAddrRel.getMboSet("TARGETCI").getMbo(0)
        ipSet = ipAddr.getMboSet("SCI_CISPEC_IP_STRNOTATION");
        if ipSet.isEmpty():
          return
        ip = ipSet.getMbo(0).getString("ALNVALUE");
        print "in findFromCS: found IP: ", ip
        if ip.count(":") == 0:
            print "ip = ", ip
        else:
            print "IP V6 is not supported"
        return ip            
    
    
def findUsingRunsOn(appCi):
    print "finding IP using using RunsOn relation"
    # built in relationship that uses runs on to find computersystem
    relationSet = appCi.getMboSet("SCI_CIRELATION_ASTOCS")
    if relationSet.isEmpty():
        return
    csSet = relationSet.getMbo(0).getMboSet("TARGETCI")
    if csSet.isEmpty():
        return
    return findFromCS(csSet.get(0))

rba_rc = "1"
try:
  ciSet = scriptHome.getMboSet("VIEWACTCI");
  if ciSet.isEmpty():
      print "No CIs found"      
      sys.exit(1)
  ci = ciSet.getMbo(0)
  # first thing is get the classstructure that is being used by the CI
  csSet = ci.getMboSet("CLASSSTRUCTURE");
  cs = csSet.getMbo(0);
  classGroupId = cs.getString("CLASSIFICATIONGROUPID");
  if classGroupId == "COMPSYS" :
      ipaddress = findFromCS(ci);
  elif classGroupId == "BUSAPP" :
      ipaddress = findUsingRunsOn(ci);
  elif classGroupId == "APPSRV" :
      ipaddress = findUsingRunsOn(ci);
  elif classGroupId == "DB" :
      ipaddress = findUsingRunsOn(ci);
  else:
      print "CI classification needs to be one of these: COMPSYS, BUSAPP, APPSRV or DB"
  if  ipaddress  is None:
      rba_rc = "3"
  else:
      rba_rc = "0"     

except:
   print "Error finding ip address: ", sys.exc_info()
   rba_rc = "4"

print "rba_rc = ", rba_rc

if ipaddress is None: 
  try:
    # Record the output in a new worklog entry
    worklogSet = scriptHome.getMboSet("MODIFYWORKLOG")
    worklogMbo = worklogSet.add()
    worklogMbo.setValue("description", "RBAGETCIIP Results")
    worklog_desc =  "RBAGETCIIP: results: rba_rc = " + rba_rc   
    worklog_desc = "Cannot get IP Address for the specified CI. Make sure that a CI is specified on the incident. Look at the action log for more details."
    worklogMbo.setValue("description_longdescription",  worklog_desc)
  except:
    print "Error writing to results windows: ", sys.exc_info()