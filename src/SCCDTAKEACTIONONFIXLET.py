# AUTOSCRIPT NAME: SCCDTAKEACTIONONFIXLET
# CREATEDDATE: 2012-10-11 16:33:28
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2015-05-19 05:50:40
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

##==============================================================================
# * 
# * IBM Confidential
# * 
# * OCO Source Materials
# * 
# * 5725-E24
# * 
# * (C) COPYRIGHT IBM CORP. 2012
# * 
# * The source code for this program is not published or otherwise
# * divested of its trade secrets, irrespective of what has been 
# * deposited with the U.S. Copyright Office.
# * 
# ***************************** End Standard Header ******************************
#=================================================================================
#-----------------------------------------------------------------------------
#
# Input: 
#    temfixletid         - task Id of the Tivoli Endpoint Manager Server
#    temfixletsiteid     - site Id of the fixlet   
#    temcomputerid       - sourceid of the deployed asset
#    temendpoint         - endpoint name containing TEM server credentials
#    temmaxretry         - maximum number of retries to check the status of TEM action. (default is 5) 
#
# Outputs:
#    temactionid          - action id of the invoked TEM action
#    temremainretry       - remaining number of iterations to check the status of the TEM action
#                          this will set to 0 if the action could not be invoked successfully. 
#                          otherwise, it will be set to the value of script parameter, temmaxretry                                                       
#
#
# Description
# This script invokes the action on the TEM server using the credential 
# Make sure the jython libraries are downloaded and copied to the  
# directory: C:\jython\Lib
# If in a different directory, update the sys.path.append() call below.
# Gets the TEM server credential from the end point and invokes the REST API
# to invoke the action on TEM Server to install the software. 
# Retrieves the actionid from the response and saves it in the temactionid parameter. 
#--------------------------------------------------------------------------------------

from psdi.iface.mic import EndPointCache
from psdi.iface.router import Router
from psdi.server import MXServer

# this function returns the message for the given message key and message group
def getMsg(msgKey, msgGrp):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgKey, msgGrp).getMessage()
    return msg


########################
####     main      ##### 
########################
#load the advanced jython libraries.
import sys

foundJython = False
propName = "pmsc.iem.jythonlib"
jythonLibPath = MXServer.getMXServer().getProperty(propName)
for path in sys.path:
    if (path.find(jythonLibPath) != -1) :
        foundJython = True
if (foundJython == False):
    sys.path.append(jythonLibPath)

import httplib  
from xml.etree import ElementTree as ET
import base64
import string    

returncode = "0"
worklogSet = mbo.getMboSet("MODIFYWORKLOG")

# get the SR Worklog mboset
srWorkLogMbo = None
workorderSet = mbo.getMboSet("PARENTPROCESS")
workorder = workorderSet.getMbo(0)
originatingTicketSet = workorder.getMboSet("ORIGTICKET")
originatingTicket = originatingTicketSet.getMbo(0)
if (originatingTicket != None):
    srWorklogSet = originatingTicket.getMboSet("MODIFYWORKLOG")

if ((temfixletid == None) or (temcomputerid == None) or (temendpoint == None)) : 
   returncode = "-1"
   worklogMbo = worklogSet.addAtEnd()
   worklogMbo.setValue("description",  getMsg("pmscoffering", "invoke_tem_fail_sum"))
   worklogMbo.setValue("clientviewable", 1)
   worklogMbo.setValue("description_longdescription", "Unable to connect to IBM Endpoint Manager Server")      

   # add to SR Worklog  
   if (originatingTicket != None):   
       srWorklogMbo = srWorklogSet.addAtEnd()
       srWorklogMbo.setValue("description", getMsg("pmscoffering", "invoke_tem_fail_sum"))
       srWorklogMbo.setValue("clientviewable", 1)
       srWorklogMbo.setValue("description_longdescription",  "Unable to connect to IBM Endpoint Manager Server")  
else:
  try:
     # Get EndPoint data - username, password, and hostname
     handler = Router.getHandler(temendpoint)

     endPointInfo = EndPointCache.getInstance().getEndPointInfo(temendpoint)
     tempassword  = endPointInfo.getProperty("PASSWORD").getValue()

     temusername= handler.getUserName()
     temserver = handler.getUrl()

     #Parse the url from the TEMServer
     urlarray = temserver.split(":")
     hostname = str(urlarray[1])
     port = int(urlarray[2])
     hostname = hostname.replace("/","")
     print hostname, port

     temfixletid = temfixletid.replace(",", "")

     print "In SCCDTAKEACTIONONFIXLET script: temendpoint = ", temendpoint
     print "In SCCDTAKEACTIONONFIXLET script: temuser = ", temusername
     print "In SCCDTAKEACTIONONFIXLET script: temserver = ", temserver
     print "In SCCDTAKEACTIONONFIXLET script: temfixlet = ", temfixletid
     print "In SCCDTAKEACTIONONFIXLET script: temfixletsiteid", temfixletsiteid
     print "In SCCDTAKEACTIONONFIXLET script: temcomputerid", temcomputerid

     if (temfixletsiteid is None):
         siteelement="<Sitename></Sitename>"
     else:
         siteelement="<SiteID>"+temfixletsiteid+"</SiteID>"

     auth = 'Basic ' + string.strip(base64.encodestring(temusername + ':' + tempassword))
  except:
     returncode = '1'

takeactionrestpacket = """<BES xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="BES.xsd">
    <SourcedFixletAction>

     <SourceFixlet>
      %s
      <FixletID>%s</FixletID>
      <Action>Action1</Action>
     </SourceFixlet>
     <Target>
      <ComputerID>%s</ComputerID>
     </Target>

     <Settings>
          <ActionUITitle>Distribute A Software</ActionUITitle>
          <PreActionShowUI>true</PreActionShowUI>
                <PreAction>
                    <Text>Preaction description</Text>
                    <AskToSaveWork>false</AskToSaveWork>
                    <ShowActionButton>false</ShowActionButton>
                    <ShowCancelButton>false</ShowCancelButton>
                    <DeadlineBehavior>RunAutomatically</DeadlineBehavior>
                    <DeadlineType>Interval</DeadlineType>
                    <DeadlineInterval>PT4M</DeadlineInterval>
                    <ShowConfirmation>false</ShowConfirmation>
                </PreAction>
                <HasRunningMessage>true</HasRunningMessage>
                <RunningMessage>
                    <Text>Distributing A Software</Text>
                </RunningMessage>
                <HasTimeRange>false</HasTimeRange>
                <HasStartTime>false</HasStartTime>
                <HasEndTime>true</HasEndTime>
                <EndDateTimeLocalOffset>P2D</EndDateTimeLocalOffset>
                <HasDayOfWeekConstraint>false</HasDayOfWeekConstraint>
                <ActiveUserRequirement>NoRequirement</ActiveUserRequirement>
                <ActiveUserType>AllUsers</ActiveUserType>
                <HasWhose>false</HasWhose>
                <PreActionCacheDownload>false</PreActionCacheDownload>    
                <Reapply>false</Reapply>
                <HasReapplyLimit>true</HasReapplyLimit>
                <ReapplyLimit>3</ReapplyLimit>
                <HasReapplyInterval>false</HasReapplyInterval>
                <HasRetry>false</HasRetry>
                <HasTemporalDistribution>false</HasTemporalDistribution>
                <PostActionBehavior Behavior="Nothing"></PostActionBehavior>
                <IsOffer>false</IsOffer>
                </Settings>

    </SourcedFixletAction>
</BES>
""" %  (siteelement, temfixletid, temcomputerid)

try:
  webservice = httplib.HTTPSConnection(hostname, port)
  webservice.putrequest('POST', "/api/actions")
  webservice.putheader('Authorization', auth )
  webservice.putheader("Content-Length", str(len(takeactionrestpacket)))
  webservice.endheaders()

  print "In SCCDTAKEACTIONONFIXLET script: request = ", takeactionrestpacket

  webservice.send(takeactionrestpacket)

except:
   returncode = '1'
   worklogMbo = worklogSet.addAtEnd()
   worklogMbo.setValue("description", getMsg("pmscoffering", "invoke_tem_fail_sum"))
   worklogMbo.setValue("clientviewable", 1)
   worklogMbo.setValue("description_longdescription", "Unable to connect to IBM Endpoint Manager Server")      

   # add to SR Worklog  
   if (originatingTicket != None):   
       srWorklogMbo = srWorklogSet.addAtEnd()
       srWorklogMbo.setValue("description", getMsg("pmscoffering", "invoke_tem_fail_sum"))
       srWorklogMbo.setValue("clientviewable", 1)
       srWorklogMbo.setValue("description_longdescription",  "Unable to connect to IBM Endpoint Manager Server")   

# 200 maps to OK - standard HTTP response
if (returncode == '0'):
  # get the response
  res = webservice.getresponse()

  print "In SCCDTAKEACTIONONFIXLET script: response status = ", res.status
  print "In SCCDTAKEACTIONONFIXLET script: response = ", res

  if (res.status ==200):
      returncode = "0"
      responsemessage = res.read()
      print "In SCCDTAKEACTIONONFIXLET script: responsemessage: ",responsemessage;
      actionResults = ET.fromstring(responsemessage)   
      
      #Parse the Action ID and save    
      for action in actionResults.findall("Action"):                        
          actionID = action.find('ID').text        
          temactionid = actionID
          print "In SCCDTAKEACTIONONFIXLET script: temactionid: ", temactionid 
          temremainretry =  temmaxretry
    
      worklogMbo = worklogSet.addAtEnd()
      worklogMbo.setValue("description", "Invoked IBM Endpoint Manager action")
      worklogMbo.setValue("clientviewable", 1)
      worklogMbo.setValue("description_longdescription", "Started Distribution through IBM Endpoint Manager. Status of the action will be checked.")      

      # add to SR Worklog  
      if (originatingTicket != None):    
          srWorklogMbo = srWorklogSet.addAtEnd()
          srWorklogMbo.setValue("description", getMsg("pmscoffering", "invoke_tem_sum"))
          srWorklogMbo.setValue("clientviewable", 1)
          srWorklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "invoke_tem_desc"))   
  else:
      print "In SCCDTAKEACTIONONFIXLET script: Unable to take action on TEM due to bad response status"
      returncode = "-1"

      worklogMbo = worklogSet.addAtEnd()
      worklogMbo.setValue("description", "Failed: Got bad response from TEM Action API" + str(res.status))
      worklogMbo.setValue("clientviewable", 1)
      worklogMbo.setValue("description_longdescription", "Response from TEM Action API:" + res.read())
    
      # add to SR Worklog
      if (originatingTicket != None):
          srWorklogMbo = srWorklogSet.addAtEnd()
          srWorklogMbo.setValue("description",  getMsg("pmscoffering", "invoke_tem_fail_sum")) 
          srWorklogMbo.setValue("clientviewable", 1)
          srWorklogMbo.setValue("description_longdescription",  getMsg("pmscoffering", "invoke_tem_fail_desc"))
    
      # no need to check the action status since we got a bad response. Set the retry for that to 0
      temremainretry = 0