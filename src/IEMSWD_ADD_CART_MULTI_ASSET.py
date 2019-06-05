# AUTOSCRIPT NAME: IEMSWD_ADD_CART_MULTI_ASSET
# CREATEDDATE: 2014-10-14 15:43:06
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-12-16 12:48:02
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
# This script is used to validate the cart for the offering - IEM software 
# integration for multiple assets.
#
# This scripts checks if a software is specified and at least 
# one asset is selected. Also, checks to make sure there are 
# enough licenses available.
# Details: 
# The software information is available in the persistent mbo: IEMSWDSW
# The asset information is available in the persistent mbo IEMSWD 
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
def copySelectedValues(swMbo, iemswdMboSet):

    count = iemswdMboSet.count()

    #copy the software id to the custom mbo
    softwareId = swMbo.getLong("tloamsoftwareid")
    swName = swMbo.getString("swname")
  
    for i in range(count):
        iemswdMboSet.getMbo(i).setValue("TLOAMSOFTWAREID", softwareId)
        iemswdMboSet.getMbo(i).setValue("SWNAME", swName)    

    #copy the license id to the custom mbo
    licenseNum =  swMbo.getString("licensenum")  
    orgId = swMbo.getString("orgid")

    for i in range(count):
        iemswdMboSet.getMbo(i).setValue("licensenum", licenseNum)
        iemswdMboSet.getMbo(i).setValue("orgid", orgId)


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

#get the persistent custom mboset containing non-tabular software information
iemswdSWMboSet = sr.getMboSet("IEMSWDSW");
iemswdSWMbo = iemswdSWMboSet.getMbo(0)

#get the persistent custom mboset containing asset information
iemswdMboSet = sr.getMboSet("IEMSWD");
iemswdMbo = iemswdMboSet.getMbo(0)

# check if a software is specified 
if (iemswdSWMbo != None):
     swName = iemswdSWMbo.getString("swname")    
if (iemswdSWMbo == None or swName == None or swName == ''):
    rc = 0
    errmsg = getMsg("pmscoffering", "iem_multi_asset_software_missing")
else:   
    # check if at least 1 asset is selected  
    if (iemswdMboSet.isEmpty()):
        rc = 0
        errmsg = getMsg("pmscoffering", "iem_multi_asset_asset_missing")
    else:
        copySelectedValues(iemswdSWMbo, iemswdMboSet)
        
        # add the software name to the description of the SR
        description = sr.getString("DESCRIPTION")
        # swname maxlength is 256, sr.desc maxlength is 352
        # truncate it as it won't be visible in the SSC requestpod anyway
        newDescription = description + " - " + swName                
        sr.setValue("DESCRIPTION", newDescription[:250])         
        
        rc, errmsg = checkAssetSiteIdBelongsToLicenseOrgId(iemswdMboSet)
#return the error code and error message (if any)
print rc
print errmsg