# AUTOSCRIPT NAME: IEMSWD_ADD_CART_MULTI_SW
# CREATEDDATE: 2014-12-01 11:36:48
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-12-16 12:48:16
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
# This script is used to validate the cart for the offering - Deploy one or more
# software to an asset using IBM Endpoint Manager
#
# This scripts checks if a software is specified and at least 
# one asset is selected. 
# Details: 
# The software information is available in the persistent mbo IEMSWD
# The asset information is available in the SR mbo
#=============================================================================

from psdi.mbo import MboConstants
from psdi.mbo import Mbo
from psdi.server import MXServer
from psdi.mbo import SqlFormat

####################################################################
# this function returns the message for the given message key and 
# message group
#
####################################################################

def getMsg(msgGrp, msgKey):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgGrp, msgKey).getMessage()
    return msg

####################################################################
# this function returns the message for the given message key and 
# message group and parameters
#
####################################################################

def getMsgWithParams(msgGrp, msgKey, params):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgGrp, msgKey)
    if msg == None:
        raise "Invalid message arguments" + msgGrp + ":" + msgKey
    else:
        return msg.getMessage(params)    
    

####################################################################
# this function copies the values to the custom mbo set
#
###################################################################
def copySelectedValues(swmbo, iemswdMboSet):

    count = iemswdMboSet.count()
    assetNum = swmbo.getString("ASSETNUM")
    assetSiteId = swmbo.getString("SITEID") 

    #copy the asset informatino to the custom mbo  
    for i in range(count):
        iemswdMboSet.getMbo(i).setValue("ASSETNUM", assetNum)
        iemswdMboSet.getMbo(i).setValue("SITEID", assetSiteId)
  
####################################################################
# this function checks if the siteid of the asset is associated with 
# the orgid of the license. Gets the asset's site's organization 
# record and checks to see if it matches the license's orgid. 
###################################################################
def checkAssetSiteIdBelongsToLicenseOrgId(iemswdMboSet):
    rc = 1
    errmsg = None
    
    iemswdMbo = iemswdMboSet.moveFirst()
    userInfo = iemswdMbo.getUserInfo()
    
    while iemswdMbo != None:
        siteId = iemswdMboSet.getString("SITEID")
        orgId = iemswdMboSet.getString("ORGID")
        sqlFormat = SqlFormat(userInfo, "siteid = :1")
        sqlFormat.setObject(1, "SITE", "SITEID", siteId)
        siteSet = MXServer.getMXServer().getMboSet("SITE", userInfo)
        siteSet.setWhere(sqlFormat.format())
        siteSet.reset()
        siteMbo = siteSet.getMbo(0)
        if (siteMbo != None):
            orgSet = siteMbo.getMboSet("ORGANIZATION")
            orgMbo = orgSet.getMbo(0)
            if ((orgMbo == None) or (orgMbo.getString("ORGID") != orgId)):
                    rc = 0
                    params = [siteId, iemswdMbo.getString("assetnum"), orgId, iemswdMbo.getString("swname")]
                    errmsg = getMsgWithParams("pmscoffering", "iem_asset_site_org_mismatch", params)
                    break
         
        iemswdMbo = iemswdMboSet.moveNext()
            
    return rc, errmsg

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

# get the IEMSWDSW Mbo
swmboSet=sr.getMboSet("IEMSWDSW");
swmbo=swmboSet.getMbo(0)

#get the persistent custom mboset containing asset information
iemswdMboSet = sr.getMboSet("IEMSWD");
iemswdMbo = iemswdMboSet.getMbo(0)

# check if a software is specified 
if (iemswdMbo != None):
     swName = iemswdMbo.getString("swname")    
if (iemswdMbo == None or swName == None or swName == ''):
    rc = 0
    errmsg = getMsg("pmscoffering", "iem_multi_sw_software_missing")
else:
    # check if an asset is specified
    assetNum = swmbo.getString("ASSETNUM")  
    if (assetNum == None or assetNum == ''):
        rc = 0
        errmsg = getMsg("pmscoffering", "iem_multi_sw_asset_missing")
    else:
        copySelectedValues(swmbo, iemswdMboSet)        
        # add the asset name to the description of the SR
        description = sr.getString("DESCRIPTION")
        sr.setValue("DESCRIPTION", description + " - " + assetNum)
        
        rc, errmsg = checkAssetSiteIdBelongsToLicenseOrgId(iemswdMboSet)      

#return the error code and error message (if any)
print rc
print errmsg