# AUTOSCRIPT NAME: SCCDIEMLICCHK
# CREATEDDATE: 2015-05-15 07:24:24
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2015-05-15 09:21:21
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
# ***************************** End Standard Header ****************************
#==============================================================
# This script is used in the workflow SCCDTEMDEP
# as a conditional launch point to evaluate if there are enough licenses available
# The workflow condition node checks the value of evalResult.
# This script calls the API isLicenseAvailable() to check the license availability
# and sets the return code in the rba_rc attribute.  
#   If the evalResult is true, it continues to the next step. 
#   If the evalResult is false, it checks the return code (rba_rc attribute) and 
#       if the rba_rc is 0, there are not enough licenses available
#                           and creates a task assignment to order more licenses. 
#       If the rba_rc is 1, it means an exception occurred while checking for
#                           license and it stops the workflow.    
#=============================================================================

from psdi.mbo import Mbo
from psdi.server import MXServer
from com.ibm.ism.iem.util import LicenseHelper
import sys,imp

# this function returns the message for the given message key and message group
def getMsg(msgGrp, msgKey):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgGrp, msgKey).getMessage()
    return msg


# this function returns the message for the give message key, message group and parameters
def getMsgWithParams(msgGrp, msgKey, params):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgGrp, msgKey).getMessage(params)
    return msg

########################
####     main      ##### 
########################
scriptName = "SCCDIEMLICCHK: "
rba_rc = '0'

# get the SR Worklog mboset
srWorklogMbo = None
workorderSet = mbo.getMboSet("PARENTPROCESS")
workorder = workorderSet.getMbo(0)
originatingTicketSet = workorder.getMboSet("ORIGTICKET")
originatingTicket = originatingTicketSet.getMbo(0)
if (originatingTicket != None):
    srWorklogSet = originatingTicket.getMboSet("MODIFYWORKLOG")
    srWorklogMbo = srWorklogSet.addAtEnd()     

assetMbo = mbo.getMboSet("ASSET").getMbo(0)
if (assetMbo != None):    
    temasset = assetMbo.getString("ASSETNUM")
    print "In SCCDIEMLICCHK script: asset: ",  temasset
    orgId = mbo.getString("ORGID")
    siteId = mbo.getString("SITEID")
    wpLicSet = mbo.getMboSet("TAMITPLANWITHRESERV")    
    wpLic = wpLicSet.getMbo(0) 
    if (wpLic != None):           
        licSet = wpLic.getMboSet("TLOAMLICENSE")
        licMbo = licSet.getMbo(0)
        if (licMbo != None):            
            licenseNum = licMbo.getString("LICENSENUM")
            print "In SCCDIEMLICCHK script: associated license = ",  licenseNum
            try:
              rc = LicenseHelper.isLicenseAvailable(temasset, siteId, licenseNum, orgId, mbo.getUserInfo())
              if (rc == 1):
                evalresult = True
              else:
                evalresult = False
            except:
              evalresult = False
              print scriptName + "Exception occurred in checking the license availability: ", sys.exc_info()
              worklogSet = mbo.getMboSet("MODIFYWORKLOG")
              worklogMbo = worklogSet.addAtEnd()
              worklogMbo.setValue("description", getMsg("pmscoffering", "iem_lic_check_error_sum"))
              worklogMbo.setValue("clientviewable", 1)
              worklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "iem_lic_check_error_desc"))

              # add to SR Worklog
              if (srWorklogMbo != None):
                 srWorklogMbo.setValue("description", getMsg("pmscoffering", "iem_lic_check_error_sum"))
                 srWorklogMbo.setValue("clientviewable", 1)
                 srWorklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "iem_lic_check_error_desc"))
       
              # set the rba_rc to 1 so that the workflow will stop due to exception
              rba_rc = '1'   
        else:
            evalresult = False
            worklogSet = mbo.getMboSet("MODIFYWORKLOG")
            worklogMbo = worklogSet.addAtEnd()
            worklogMbo.setValue("description", getMsg("pmscoffering", "license_missing_sum"))
            worklogMbo.setValue("clientviewable", 1)
            worklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "license_missing_desc"))
            # add to SR Worklog
            if (srWorklogMbo != None):
               srWorklogMbo.setValue("description", getMsg("pmscoffering", "license_missing_sum"))
               srWorklogMbo.setValue("clientviewable", 1)
               srWorklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "license_missing_desc"))
            rba_rc = '1'  
else:
    evalresult = False
    worklogSet = mbo.getMboSet("MODIFYWORKLOG")
    worklogMbo = worklogSet.addAtEnd()
    worklogMbo.setValue("description", getMsg("pmscoffering", "iem_multi_sw_asset_missing"))
    worklogMbo.setValue("clientviewable", 1)
    worklogMbo.setValue("description_longdescription",getMsg("pmscoffering", "iem_multi_sw_asset_missing"))    
    # add to SR Worklog
    if (srWorklogMbo != None):
       srWorklogMbo.setValue("description", getMsg("pmscoffering", "iem_multi_sw_asset_missing"))
       srWorklogMbo.setValue("clientviewable", 1)
       srWorklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "iem_multi_sw_asset_missing"))
    rba_rc = '1'  

print scriptName + "rba_rc = ", rba_rc
mbo.setValue("rba_rc",  rba_rc)