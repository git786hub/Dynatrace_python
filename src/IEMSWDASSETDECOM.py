# AUTOSCRIPT NAME: IEMSWDASSETDECOM
# CREATEDDATE: 2014-11-19 14:58:48
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-11-19 16:09:28
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
# This script is used to unallocate the licenses associated with assets
# which are decommissioned. This script gets called when the status of 
# the asset is changed. The licenses are unallocated when the 
# internal status of the asset is changed to decommissioned
#
#=============================================================================

from psdi.mbo import Mbo
from psdi.server import MXServer
from com.ibm.ism.iemswd.app.license import LicReservHelper
import sys

# get the translated value for the status
statusValue = mbo.getMboServer().getMaximoDD().getTranslator().toInternalString("LOCASSETSTATUS", status)
if (statusValue == "DECOMMISSIONED"):
   try: 
      LicReservHelper.deleteLicenseAllocationsForAsset(assetNum, siteId, mbo.userInfo)
   except:
      print "Unable to delete the licenses allocated for the asset: assetNum: siteId = " + assetNum + ":" + siteId