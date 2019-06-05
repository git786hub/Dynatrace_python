# AUTOSCRIPT NAME: IEMLICCHK
# CREATEDDATE: 2014-11-10 14:12:36
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-11-19 15:25:44
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
# This script is used in the workflow for the IEMSWD offering for multiple assets
# as a conditional launch point to evaluate if there are enough licenses available
# This scripts returns a true or false. The value is set in the implicit 
# "evalResult" variable  
#
# The workflow condition node checks the value of evalResult.
# This script calls the API isLicenseAvailable() to check the license availability
# and sets the return code in the rba_rc attribute.  
#   If the evalResult is true, it continues to the next step to reserve the license. 
#   If the evalResult is false, it checks the return code (rba_rc attribute) and 
#       if the rba_rc is 0, there are not enough licenses available
#                           and creates a task assignment to order more licenses. 
#       If the rba_rc is 1, it means an exception occurred while checking for
#                           license and it stops the workflow.    
#
#=============================================================================

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
scriptName = "IEMLICCHK: "
from iemswdhelper import IEMSWDHelper
helper = IEMSWDHelper(mbo)
rba_rc = '0'

iemswdMboSet = mbo.getMboSet("SR").getMbo(0).getMboSet("IEMSWD")
if (iemswdMboSet.getMbo(0) == None):
    # This should not happen
    evalResult = False
    rba_rc = '1'
    print scriptName + "No assets specified with the request"
else:    
    iemswdMbo = iemswdMboSet.getMbo(0)  
    licenseNum = iemswdMbo.getString("LICENSENUM")
    orgId = iemswdMbo.getString("ORGID")  
    assetSet = helper.getAssetMboSet(iemswdMboSet)
   
    try:
        rc = LicReservHelper.isLicenseAvailable(assetSet, licenseNum, orgId, mbo.getUserInfo())  
        if (rc == 1):
            evalresult = True
        else:
            evalresult = False
            print scriptName + "Not enough Licenses available"
            helper.addToSRWorkLog("iem_insufficient_license_sum", "iem_insufficient_license_desc")
            helper.updateStatus(iemswdMboSet, "NOLICENSE", "iem_insufficient_license_desc")
    except:
        evalresult = False
        print scriptName + "Exception occurred in checking the license availability: ", sys.exc_info()
        helper.addToSRWorkLog("iem_lic_check_error_sum", "iem_lic_check_error_desc")
        helper.addErrorToWorkLog("iem_lic_check_error_sum", str(sys.exc_info()[0]))
        helper.updateStatus(iemswdMboSet, "FAILED", "iem_lic_check_error_sum")
        # set the rba_rc to 1 so that the workflow will stop due to exception
        rba_rc = '1'   

print scriptName + "rba_rc = ", rba_rc
mbo.setValue("rba_rc",  rba_rc)