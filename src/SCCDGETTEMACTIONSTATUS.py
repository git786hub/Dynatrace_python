# AUTOSCRIPT NAME: SCCDGETTEMACTIONSTATUS
# CREATEDDATE: 2012-10-11 10:54:30
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2015-05-18 04:39:10
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
#---------------------------------------------------------------------------------
#
# Input:
#    temaction          - action id of the invoked TEM action
#    temcomputer        - Asset num of the computer.
#    temendpoint        - name of the endpoint containing the TEM server credential
#
# Outputs:
#    returncode         - return code from the TEM action 
#
# Inputs/Outputs:
#    temremainretry     - remaining number of iterations to check the status of the TEM action
#                         This will be decremented by 1 if we get a good response code. 
#
# Description
# This script invokes the action on the TEM server using the credential 
# Make sure the jython libraries are downloaded and copied to the  
# directory: C:\jython\Lib
# If in a different directory, update the sys.path.append() call below.
# Gets the TEM server credential from the end point and invokes the REST API
# to get the status of the action that was invoked.  
# It retrieves the status of the action and saves it in returncode parameter.
# Also, decrements the temremainretry if we get a good response. Else, sets it to 0
#---------------------------------------------------------------------------------

from psdi.iface.mic import EndPointCache
from psdi.iface.router import Router
from psdi.server import MXServer

# this function returns the message for the given message key and message group
def getMsg(msgKey, msgGrp):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgKey, msgGrp).getMessage()
    return msg

# this function returns the message for the give message key, message group and parameters
def getMsgWithParams(msgKey, msgGrp, params):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgKey, msgGrp).getMessage(params)
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

# get the SR Worklog mboset
originatingTicket = None
workorderSet = mbo.getMboSet("PARENTPROCESS")
workorder = workorderSet.getMbo(0)
originatingTicketSet = workorder.getMboSet("ORIGTICKET")
originatingTicket = originatingTicketSet.getMbo(0)
if (originatingTicket != None):
    srWorklogSet = originatingTicket.getMboSet("MODIFYWORKLOG")
    
    
# Get TEM EndPoint data - username, password, and hostname
handler = Router.getHandler(temendpoint)

endPointInfo = EndPointCache.getInstance().getEndPointInfo(temendpoint)
tempassword  = endPointInfo.getProperty("PASSWORD").getValue()

temusername= handler.getUserName()
temserver = handler.getUrl()

urlarray = temserver.split(":")
hostname = str(urlarray[1])
port = int(urlarray[2])
hostname = hostname.replace("/","")
print "In SCCDGETTEMACTIONSTATUS script: hostname : port = " ,  hostname + " , " , port

auth = 'Basic ' + string.strip(base64.encodestring(temusername + ':' + tempassword))


webservice = httplib.HTTPSConnection(hostname, port)
webservice.putrequest('GET', "/api/action/%s/status" % temaction)
webservice.putheader('Authorization', auth )
webservice.endheaders()


# get the response
res = webservice.getresponse()

print "In SCCDGETTEMACTIONSTATUS script: response status = ", res.status

# 200 maps to OK - standard HTTP response
if (res.status == 200):
    responsemessage = res.read()
    print "In SCCDGETTEMACTIONSTATUS script: responsemessage: ", responsemessage
    actionResults = ET.fromstring(responsemessage) 
    print "In SCCDGETTEMACTIONSTATUS script: actionResults: ", actionResults 
    

    # Potentially filter by a particular computer result from the passed in asset, This only looks for one response for the whole action
    for computer in actionResults.getiterator("Computer"):            
        computerId = computer.attrib.get("ID")          
        state = computer.find('State')     
        actionStatus = computer.find('State').text
        isError = state.get('IsError')
        status = computer.find("Status").text              

        print "In SCCDGETTEMACTIONSTATUS script: actionStatus: ", actionStatus
        print "In SCCDGETTEMACTIONSTATUS script: error: ", isError
        if (int(isError) != 0):
            print "In SCCDGETTEMACTIONSTATUS script: received an error distributing, rc = -1 "
            returncode = "-1"
            worklogSet = mbo.getMboSet("MODIFYWORKLOG")
            worklogMbo = worklogSet.addAtEnd()
            worklogMbo.setValue("description", getMsg("pmscoffering", "invoke_tem_fail_sum"))
            worklogMbo.setValue("clientviewable", 1)
            worklogMbo.setValue("description_longdescription", status)

            # add to SR Worklog
            if (originatingTicket != None):
                srWorklogMbo = srWorklogSet.add()                
                srWorklogMbo.setValue("description",  getMsg("pmscoffering", "invoke_tem_fail_sum")) 
                srWorklogMbo.setValue("clientviewable", 1)
                srWorklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "invoke_tem_fail_desc"))
        else:
            if (int(actionStatus) == 3):
                print "In SCCDGETTEMACTIONSTATUS script: received a success message, rc = 0 "
                returncode = "0"
                if (originatingTicket != None):
                    srWorklogMbo = srWorklogSet.add()
                    srWorklogMbo.setValue("description", getMsg("pmscoffering", "tem_deploy_success_sum"))
                    srWorklogMbo.setValue("clientviewable", 1)
                    srWorklogMbo.setValue("description_longdescription", getMsg("pmscoffering","tem_deploy_success_desc"))
            elif (int(actionStatus) == 0):
                    print "In SCCDGETTEMACTIONSTATUS script: received a success message, rc = 0 "
                    returncode = "-1"
                    worklogSet = mbo.getMboSet("MODIFYWORKLOG")
                    worklogMbo = worklogSet.addAtEnd()
                    worklogMbo.setValue("description", getMsg("pmscoffering", "invoke_tem_fail_sum"))
                    worklogMbo.setValue("clientviewable", 1)
                    worklogMbo.setValue("description_longdescription", status)

                    # add to SR Worklog
                    if (originatingTicket != None):
                       srWorklogMbo = srWorklogSet.add()                
                       srWorklogMbo.setValue("description",  getMsg("pmscoffering", "invoke_tem_fail_sum")) 
                       srWorklogMbo.setValue("clientviewable", 1)
                       params = [temcomputer, temaction, status]
                       srWorklogMbo.setValue("description_longdescription", getMsgWithParams("pmscoffering", "invoke_tem_fail_desc_with_status", params))

    temremainretry = temremainretry - 1
else:
    print "In SCCDGETTEMACTIONSTATUS script: received a bad response status"
    worklogSet = mbo.getMboSet("MODIFYWORKLOG")
    worklogMbo = worklogSet.addAtEnd()
    worklogMbo.setValue("description", "Failed: Got bad response from TEM Action API"  + str(res.status))
    worklogMbo.setValue("clientviewable", 1)
    params = [temcomputer, temaction, status]
    worklogMbo.setValue("description_longdescription", getMsgWithParams("pmscoffering", "invoke_tem_fail_desc_with_status", params))

    # add to SR Worklog
    if (originatingTicket != None):
        srWorklogMbo = srWorklogSet.add()
        srWorklogMbo.setValue("description", getMsg("pmscoffering", "invoke_tem_fail_sum")) 
        srWorklogMbo.setValue("clientviewable", 1)
        srWorklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "invoke_tem_fail_desc")) 
    
    # no need to check the action status since we got a bad response. Set the retry to 0
    temremainretry = 0
    
    # set rc to -2 for bad response code
    returncode = "-2"