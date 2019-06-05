# AUTOSCRIPT NAME: IEMSWDLICDECMULTISW
# CREATEDDATE: 2014-12-01 13:32:32
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-12-02 15:07:50
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
# Outputs:
#   rba_rc
#
# Description#  
# This script is used in the workflow for the IEMSWD offering for multiple software
# This scripts calls an API to allocate the licenses and it sets the rba_rc  
# attribute to '0' if it was allocated successfully. Also, adds a worklog entry for the 
# license allocation.  
#--------------------------------------------------------------------------------------

from psdi.server import MXServer

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

scriptName = "IEMSWDLICDECMULTISW: "
from iemswdhelper import IEMSWDHelper
helper = IEMSWDHelper(mbo)

rba_rc = '0'
iemswdMboSet = mbo.getMboSet("SR").getMbo(0).getMboSet("IEMSWD")
if (iemswdMboSet.getMbo(0) == None):
    # This should not happen    
    rba_rc = '1'
    print scriptName + "No assets specified with the request"
else:
    try:
        rc = LicReservHelper.allocateLicensesForAsset(iemswdMboSet, mbo)
        print scriptName + "LicReservHelper.allocateLicenseForAsset: rc = ", rc 
        if (rc == True):            
            helper.addToSRWorkLog("iem_license_alloc_sum",  "iem_license_alloc_desc")                        
        else:
            rba_rc = '1'
            helper.addToSRWorkLog("iem_license_overalloc_sum", "iem_license_overalloc_desc")            
    except:       
        # set the rba_rc to non zero to indicate error
        rba_rc = '2'
        print scriptName + "Exception occurred in allocating the license: ", sys.exc_info()
        helper.addErrorToWorkLog("iem_license_alloc_error_sum", str(sys.exc_info()[1]))
        helper.addToSRWorkLog("iem_license_alloc_error_sum", "iem_license_alloc_error_desc")