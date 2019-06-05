# AUTOSCRIPT NAME: IEMSWDTAKEACTION
# CREATEDDATE: 2014-11-12 09:02:26
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-12-15 18:20:24
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
# * (C) COPYRIGHT IBM CORP. 2014
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
#    
#    maxRetry        - maximum number of retries to check the status of IEM action. (default is 30) 
#
# Outputs:
#    retry                - remaining number of iterations to check the status of the IEM action
#                              this will set to 0 if the action could not be invoked successfully. 
#                              otherwise, it will be set to the value of script parameter, maxRetry
#    rba_rc             - return code  
#
# Description
# This script invokes the action on the IEM server using the credential 
# The system property "pmsc.iem.jythonlib" contains the path to the 
# jython libraries.  Make sure the jython libraries are exploded and copied to the  
# directory: C:\jython\Lib. If not, update the property with the correct path. 
#
# Gets the IEM server credential from the end point and invokes the REST API
# to invoke the action on IEM Server to install the software. 
# Retrieves the actionid from the response and saves it in the custom mbo. 
#-------------------------------------------------------------------------------------------------
from psdi.mbo import Mbo
from psdi.server import MXServer
from com.ibm.ism.iemswd.app.license import LicReservHelper
import sys,imp
     
# find and load internal helper scripts
# into the namespace of this script
autoscript = MXServer.getMXServer().getMboSet("AUTOSCRIPT", mbo.getUserInfo())
autoscript.setWhere("autoscript = 'IEMSWDHELPER'")
autoscript.reset()
helperscript = autoscript.getMbo(0).getString("source")

# create a new module for offering helper script
iemswdhelper = imp.new_module('iemswdhelper')
# load our db script into the new module
exec helperscript in iemswdhelper.__dict__
# add our new module to the list of system modules so we can 'from' it
# below
sys.modules["iemswdhelper"] = iemswdhelper
#######################################################################

scriptName = "IEMMSWDTAKEACTION: "
from iemswdhelper import IEMSWDHelper
helper = IEMSWDHelper(mbo)
helper.setJythonPath()

import httplib
from xml.etree import ElementTree as ET
import base64
import string  

rba_rc = '0'
iemActionId = None

iemswdMboSet = mbo.getMboSet("SR").getMbo(0).getMboSet("IEMSWD")
iemswdMbo = iemswdMboSet.getMbo(0)  
if (iemswdMbo == None):
    rba_rc = '1'
else:
    # get the deployable software tasks
    deploySwTaskMbo = helper.getDeployableSoftwareTaskMbo(iemswdMbo)

    if (deploySwTaskMbo == None):
        helper.updateStatus(iemswdMboSet, "FAILED", "iem_swctg_missing_deploytask_sum")           
        rba_rc = '1'  
    else:                 
        fixletId = helper.getFixletId(deploySwTaskMbo)  
        endPointName = helper.getEndpointName(deploySwTaskMbo)                    
        siteElement = helper.getSiteElement(deploySwTaskMbo)                  
  
    # get the computerIds
    if (rba_rc == '0'):  
        computerIdElement = helper.getComputerIdElement(iemswdMboSet, False)
        if (computerIdElement == None):           
            rba_rc = '1'  

    if (rba_rc == '0'):
        takeActionRestPacket = helper.getRequestPayloadXmlForMultiAssets(siteElement, fixletId, computerIdElement)
        try:         
            res  = helper.invokeIEMAction(endPointName, takeActionRestPacket)
        except:
            rba_rc = '1'
            helper.addToSRWorkLog("iem_invoke_fail_sum", "iem_server_connect_failed")
            helper.updateStatus(iemswdMboSet, "FAILED", "iem_server_connect_failed")            
            
    if (rba_rc == '0'):
        if (res == None):
            # error already reported
            rba_rc = '1'
            retry = 0
        else:
            print scriptName + "response status = ", res.status

            # 200 maps to OK - standard HTTP response
            if (res.status == 200):
                responseMessage = res.read()
                print scriptName + "responseMessage: ", responseMessage;
                actionResults = ET.fromstring(responseMessage)   
      
                #Parse the Action ID and save    
                for action in actionResults.findall("Action"):                        
                    iemActionId = action.find('ID').text
                    print scriptName + "iemActionId: ", iemActionId
                    
                if (iemActionId is not None): 
                    retry =  maxRetry
                    helper.addToSRWorkLog("iem_invoke_sum", "iem_invoke_desc")
                    helper.updateStatus(iemswdMboSet, "INPROG", "iem_invoke_sum")                    
                    # set the iemactionid on all the mbos
                    swdMbo = iemswdMboSet.moveFirst()         
                    while (swdMbo != None):
                        swdMbo.setValue("IEMACTIONID", iemActionId)
                        swdMbo = iemswdMboSet.moveNext()
                else:
                    helper.addToSRWorkLog("iem_invoke_fail_sum", "iem_invoke_fail_desc")
                    helper.updateStatus(iemswdMboSet, "FAILED", "iem_invoke_fail_sum")
                    helper.addErrorToWorkLog("iem_invoke_fail_sum", "Unable to get the actionId from IEM: actionID is null")
                    rba_rc = '1'
                    retry = 0
            else:
                print scriptName + "Unable to take action on TEM due to bad response status", res.status
                helper.updateStatus(iemswdMboSet, "FAILED", "iem_invoke_fail_sum")
                helper.addToSRWorkLog("iem_invoke_fail_sum", "iem_invoke_fail_desc")
                helper.addErrorToWorkLog("iem_invoke_fail_sum", "Response from TEM Action API:" + str(res.status))    
                rba_rc = '1'
                # no need to check the action status since we got a bad response. Set the retry for that to 0
                retry = 0