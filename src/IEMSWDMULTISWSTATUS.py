# AUTOSCRIPT NAME: IEMSWDMULTISWSTATUS
# CREATEDDATE: 2014-12-01 13:02:17
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-12-15 17:25:07
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

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
#   None
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
import java.util.ArrayList as ArrayList
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

scriptName = "IEMSWDMULTISWSTATUS: "
from iemswdhelper import IEMSWDHelper
helper = IEMSWDHelper(mbo)
helper.setJythonPath()

import httplib
from xml.etree import ElementTree as ET
import base64
import string  

rba_rc = '0'

iemswdMboSet = mbo.getMboSet("SR").getMbo(0).getMboSet("IEMSWD")  
iemswdMbo = iemswdMboSet.moveFirst();

# get the deployable software tasks
deployableSwTaskMboSet = ArrayList()
while (iemswdMbo != None):
    print scriptName + "software = " + iemswdMbo.getString("SWNAME") 
    deployableSwTaskMbo = helper.getDeployableSoftwareTaskMbo(iemswdMbo)
    if (deployableSwTaskMbo != None):
        deployableSwTaskMboSet.add(deployableSwTaskMbo)
    else:  
        rba_rc = '1'
        deployableSwTaskMboSet.clear()       
        break
    iemswdMbo = iemswdMboSet.moveNext()
    
i = 0
success = 0
failure = 0 
done = True   
          
for i in range(deployableSwTaskMboSet.size()): 
    iemswdMbo = iemswdMboSet.getMbo(i)   
    deployableSwTaskMbo = deployableSwTaskMboSet.get(i)
    swName = iemswdMbo.getString("SWNAME")     
    iemActionId = iemswdMbo.getInt("IEMACTIONID")
    if (iemActionId == None): 
        continue
    else:
        print scriptName + "iemActionId = ", iemActionId              
    endPointName = helper.getEndpointName(deployableSwTaskMbo)
    
    # call IEM Server to get the status of the IEM Action
    res = None
    try: 
        res = helper.getActionStatus(endPointName, iemActionId)
    except:
        rba_rc = '1'
        helper.addToSRWorkLog("iem_check_status_fail_sum", "iem_server_connect_failed")
        helper.updateStatus(iemswdMboSet, "FAILED", "iem_server_connect_failed")                      

    
    if (res == None):
        #helper.updateMboStatus(iemswdMbo, "FAILED", "iem_check_status_fail_sum")
        rba_rc = '1'        
    else:        
        print scriptName + "response status = ", res.status
        

    # 200 maps to OK - standard HTTP response
    if (res != None): 
        if (res.status == 200):
            responseMessage = res.read()
            print scriptName + "Software: " + swName + " responseMessage: ", responseMessage;
            actionResults = ET.fromstring(responseMessage)   
            rba_rc = helper.updateIEMStatus(iemswdMbo, actionResults) 
            if (rba_rc == None):            
                done = False
            else:
                if (rba_rc == '0'):
                    success = success + 1
                else:
                    failure = failure + 1
        else:
            responseErrMsg = res.read()
            print scriptName + "Unable to get status from IEM due to bad response. status : response = " + responseErrMsg
            helper.addToSRWorkLog("iem_check_status_fail_sum", "iem_check_status_fail_desc")    
            helper.addErrorToWorkLog("iem_check_status_fail_sum", "Response from IEM Action API: status : response = " + responseErrMsg)
            helper.updateMboStatus(iemswdMbo, "FAILED", "iem_check_status_fail_sum")           
            
            failure = failure + 1
            # set rc to -2 for bad response code
            rba_rc = '-2'
     
        
if (done == False):    
    retry = retry - 1
else:
    retry = 0
    rba_rc = helper.getAllDeploymentStatusReturnCode(iemswdMboSet)      
    
print scriptName + "success count = ",  success
print scriptName + "failure count = ",  failure
print scriptName + "remaining retries = ", retry