# AUTOSCRIPT NAME: IEMSWDMULTIASSETSTATUS
# CREATEDDATE: 2014-11-15 16:31:42
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-12-15 16:03:16
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
# Outputs:
#    rba_rc              - return code
#    retry                 - remaining number of iterations to check the status of the IEM action
#                               this will set to 0 if the action completed successfully. 
#                               otherwise, it will be decremented by 1                                                             
#
#
# Description
# This script invokes the action on the IEM server using the credential 
# The system property "pmsc.iem.jythonlib" contains the path to the 
# jython libraries.  Make sure the jython libraries are exploded and copied to the  
# directory: C:\jython\Lib. If not, update the property with the correct path. 
#
# Gets the IEM server credential from the end point and invokes the REST API
# to get the status of the IEM action.
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

scriptName = "IEMSWDMULTIASSETSTATUS: "
from iemswdhelper import IEMSWDHelper
helper = IEMSWDHelper(mbo)
helper.setJythonPath()

import httplib
from xml.etree import ElementTree as ET
import base64
import string  


rba_rc = '0'

iemswdMboSet = mbo.getMboSet("SR").getMbo(0).getMboSet("IEMSWD") 
iemswdMbo = iemswdMboSet.getMbo(0)
iemActionId = iemswdMbo.getInt("IEMACTIONID")
  
if (iemswdMbo == None):
    rba_rc = '1'
else:
    # get the deployable software tasks
    deploySwTaskMbo = helper.getDeployableSoftwareTaskMbo(iemswdMbo)
    if (deploySwTaskMbo == None):
        rba_rc = '1'  
    else:                
        endPointName = helper.getEndpointName(deploySwTaskMbo)                   

# call IEM Server to get the status of the IEM Action
res = None 
if (rba_rc == '0'):   
    try: 
        res = helper.getActionStatus(endPointName, iemActionId)
    except:
        rba_rc = '1'
        helper.addToSRWorkLog("iem_check_status_fail_sum", "iem_server_connect_failed")
        helper.updateStatus(iemswdMboSet, "FAILED", "iem_server_connect_failed")
                                   

if (rba_rc == '0'):  
    print scriptName + "response status = ", res.status    

    # 200 maps to OK - standard HTTP response
    if (res.status == 200):
        responseMessage = res.read()
        print scriptName + "responseMessage: ", responseMessage;
        actionResults = ET.fromstring(responseMessage)   
        rba_rc = helper.updateIEMStatusForMultiAsset(iemswdMboSet, actionResults) 
        if (rba_rc == None):
            #retry again since it is not done    
            retry = retry - 1
        else:
            # we got a response
            retry = 0
            rba_rc = helper.getAllDeploymentStatusReturnCode(iemswdMboSet)  
    else:
        responseErrMsg = res.read()
        helper.updateStatus(iemswdMboSet, "FAILED", helper.getMsg("iem_check_status_fail_sum"))
        print scriptName + "Unable to get status from IEM due to bad response. status : response = " + responseErrMsg
        helper.addToSRWorkLog("iem_check_status_fail_sum", "iem_check_status_fail_desc")    
        helper.addErrorToWorkLog("iem_check_status_fail_sum", "Response from IEM Action API: status : response = " + responseErrMsg)
                   
        # no need to check the action status since we got a bad response. Set the retry for that to 0
        retry = 0    
        # set rc to -2 for bad response code
        rba_rc = '-2'
        
print scriptName + "remaining retries = ", retry
print scriptName + "rba_rc = ", rba_rc