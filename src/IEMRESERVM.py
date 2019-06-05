# AUTOSCRIPT NAME: IEMRESERVM
# CREATEDDATE: 2014-12-01 12:55:55
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-12-05 12:51:06
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
# ***************************** End Standard Header ****************************
#==============================================================
# This script is used in the workflow for the IEMSWD offering for multiple 
# software as a conditional launch point to reserve licenses.
# This scripts returns a true or false. The value is set in the implicit 
# "evalResult" variable 
#
# The workflow condition node checks the value of evalResult.
# This script calls the API reserveLicense() to reserve the license 
# and sets the return code in the rba_rc attribute.  
#   If the evalResult is true, it continues to the next step to invoke IEM task. 
#   If the evalResult is false, it checks the return code (rba_rc attribute) and 
#       if the rba_rc is 0, unable to reserve a license and 
#                           it creates a task assignment to order more licenses. 
#       If the rba_rc is 1, it means an exception occurred while reserving the
#                           license and it stops the workflow.    
#
#============================================================================  
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
scriptName = "IEMRESERVM: "
from iemswdhelper import IEMSWDHelper
helper = IEMSWDHelper(mbo)
rba_rc = '0'

iemswdMboSet = mbo.getMboSet("SR").getMbo(0).getMboSet("IEMSWD")
if (iemswdMboSet.getMbo(0) == None):
    # This should not happen
    evalResult = False
    rba_rc = '1'
    print scriptName + "No software specified with the request"
else:
    iemswdMbo = iemswdMboSet.getMbo(0)
    assetNum = iemswdMbo.getString("ASSETNUM")
    siteId = iemswdMbo.getString("SITEID")
    licenseNumList, orgList, tloamsoftwareList = helper.getLicenseInfo(iemswdMboSet)      
  
    try:
        rc = LicReservHelper.reserveLicensesForAsset(assetNum, siteId, licenseNumList, orgList, tloamsoftwareList, mbo, 0)
        if (rc == 1):
            evalresult = True
            helper.addToSRWorkLog("iem_license_reserved_sum",  "iem_license_reserved_desc")
        else:
            evalresult = False
            helper.addToSRWorkLog("iem_insufficient_license_sum", "iem_insufficient_license_desc")
            helper.updateStatus(iemswdMboSet, "NOLICENSE", "iem_insufficient_license_desc")
    except:
        evalresult = False
        helper.addToSRWorkLog("iem_license_reserv_error_sum", "iem_license_reserv_error_desc")   
        # set the rba_rc to 1 so that the workflow will stop due to exception
        rba_rc = '1'
        print scriptName + "Exception occurred in checking the license availability: ", sys.exc_info()
        helper.addErrorToWorkLog("iem_license_reserv_error_sum", str(sys.exc_info()[1]))
        helper.updateStatus(iemswdMboSet, "FAILED", "iem_license_reserv_error_desc" )

print scriptName + "rba_rc = ", rba_rc
mbo.setValue("rba_rc",  rba_rc)