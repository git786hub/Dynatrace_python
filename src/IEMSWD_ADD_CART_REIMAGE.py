# AUTOSCRIPT NAME: IEMSWD_ADD_CART_REIMAGE
# CREATEDDATE: 2014-12-04 10:59:03
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-12-11 14:18:04
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
#==============================================================================
# This script is used to validate the cart for the offering - Reimage an asset by
# deploying the entitled software using IBM Endpoint Manager 
#
# This scripts checks if the specified asset has one or more software license 
# allocated to it. 
#
#=============================================================================

from psdi.mbo import MboConstants
from psdi.mbo import Mbo
from psdi.server import MXServer
from com.ibm.ism.iemswd.app.license import LicReservHelper
from java.util import Iterator
from java.util.Map import Entry

####################################################################
# this function returns the message for the given message key and 
# message group
#
####################################################################

def getMsg(msgGrp, msgKey):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgGrp, msgKey).getMessage()
    return msg


####################################################################
# this function copies the values to the custom mbo set
#
###################################################################
def copyValues(swmbo, iemswdMboSet, map):

    assetNum = swmbo.getString("ASSETNUM")
    siteId = swmbo.getString("SITEID") 
    i = 0
    count = map.size()
    iterator = map.entrySet().iterator()
    
    while (iterator.hasNext() == True):
        entry = iterator.next();
        tloamsoftwareid = entry.getKey()
        licenseInfo = entry.getValue()
           
        #copy the asset informatino to the custom mbo  
        iemswdMbo = iemswdMboSet.add()
        iemswdMbo.setValue("ASSETNUM", assetNum)
        iemswdMbo.setValue("SITEID", siteId)
        iemswdMbo.setValue("TLOAMSOFTWAREID", tloamsoftwareid)        
        iemswdMbo.setValue("LICENSENUM", licenseInfo[0])
        iemswdMbo.setValue("ORGID", licenseInfo[1])
        iemswdMbo.setValue("SWNAME", licenseInfo[3]) 

##################################################################
## main
##################################################################

# set the error code and error message to be returned from this script
# This script is invoked as part of the offering submission and therefore
# rc = 0 implies a bad return code and it displays a error message 
# specified in the errmsg variable
rc = 1
errmsg = ''

# get the sr
srSet=scriptHome.getMboSet("SR");
sr=srSet.getMbo(0)

# get non-tabular mbo iemswdsw
swmboSet = sr.getMboSet("IEMSWDSW");
swmbo = swmboSet.getMbo(0)

assetNum = swmbo.getString("ASSETNUM")
siteId = swmbo.getString ("SITEID")

if (assetNum == ''):
    rc = 0
    errmsg = getMsg("pmscoffering", "iem_multi_sw_asset_missing")
else:
    map = LicReservHelper.getSoftwareFromAssetAllocations(assetNum, siteId, sr.getUserInfo())
    count = map.size()
    
    if (count == 0):
        rc = 0
        errmsg = getMsg("pmscoffering", "iem_reimage_asset_no_sw")
    else:                                                    
        #get the persistent custom mboset containing asset information
        iemswdMboSet = sr.getMboSet("IEMSWD");
        copyValues(swmbo, iemswdMboSet, map)
        
        # add the asset name to the description of the SR
        description = sr.getString("DESCRIPTION")
        sr.setValue("DESCRIPTION", description + " - " + assetNum)
      

#return the error code and error message (if any)
print rc
print errmsg