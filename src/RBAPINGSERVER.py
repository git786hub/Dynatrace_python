# AUTOSCRIPT NAME: RBAPINGSERVER
# CREATEDDATE: 2011-11-10 15:28:09
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2011-11-22 11:13:54
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from java.lang import Runtime
from java.lang import Process
from java.io import BufferedReader
from java.io import InputStreamReader
from java.lang import Thread
from java.lang import Integer
from psdi.mbo import MboSet

print "starting script ping server"
# ipaddress is the input parameter to this script
# rba_rc is the output parameter that stores the return code from ping command

rba_rc = "2"

if ipaddress is None:
  print "ipaddress cannot be found"
else:
  # format the start of the worklog entry
  incident = scriptHome.getString("TICKETID").strip()
  worklogDesc = "RBAPING script run for Incident: " + incident + "\n"
  worklogDesc = worklogDesc + "CI operated on: " + ipaddress + "\n"
  
  process = Runtime.getRuntime().exec("cmd.exe /C ping " + ipaddress)
  reader = BufferedReader(InputStreamReader(process.getInputStream()))
  while 1:
         lineRead = reader.readLine()
         if lineRead is None: break
         print lineRead
         worklogDesc = worklogDesc + lineRead

  rba_rc = Integer.toString(process.exitValue())

  try:
    # Record the output in a new worklog entry
    worklogSet = scriptHome.getMboSet("MODIFYWORKLOG")
    worklogMbo = worklogSet.add()
    worklogMbo.setValue("description", "RBAPING Results")
    worklogMbo.setValue("description_longdescription", worklogDesc)
  except:
    print "Error writing to results windows: ", sys.exc_info()
    rba_rc = "3"