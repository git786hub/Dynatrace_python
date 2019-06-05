# AUTOSCRIPT NAME: SCCDLICDEC
# CREATEDDATE: 2012-09-04 16:42:48
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2012-12-07 14:04:26
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
# * (C) COPYRIGHT IBM CORP. 2012
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
#   None
#
# Description#  
# Make sure the jython libraries are downloaded and copied to the  
# directory: C:\jython\Lib
# If in a different directory, update the sys.path.append() call below.
# This script decrements the license capacity by adding an entry to the
# TLOAMLICINTDIST table. Also, adds a worklog entry to the woactivity about the 
# license allocation.  
#--------------------------------------------------------------------------------------

from psdi.server import MXServer

# this function returns the message for the given message key and message group
def getMsg(msgKey, msgGrp):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgKey, msgGrp).getMessage()
    return msg


# this function returns the message for the give message key, message group and parameters
def getMsgWithParams(msgKey, msgGrp, params):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgKey, msgGrp).getMessage(params)
    return msg

########################
####     main      ##### 
########################

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
    print "In SCCDLICDEC script: asset: ",  temasset
    
    wpLicSet = mbo.getMboSet("TAMITPLANWITHRESERV")    
    wpLic = wpLicSet.getMbo(0) 
    if (wpLic != None):           
        licSet = wpLic.getMboSet("TLOAMLICENSE")
        licMbo = licSet.getMbo(0)
        if (licMbo != None):            
            licenseNum = licMbo.getString("LICENSENUM")
            licMbo.useWOCapacityCalculator()
              
            print "In SCCDLICDEC script: associated license = ",  licenseNum            
    
            # get associated worklog mbo
            worklogSet = mbo.getMboSet("MODIFYWORKLOG")
            worklogMbo = worklogSet.addAtEnd()        
                
            # Decrement the licenses available by adding an entry in the TLOAMLICINTDIST table
            # get all the licenses associated with this asset
            
            # check for license already allocated using the relationship TLOAMLICINTDISTASSET          
            licDistSet = licMbo.getMboSet("TLOAMLICINTDISTASSET")
            licDistSet.reset();
            licDistSet.setWhere("assetnum='" + temasset + "'")
            if (licDistSet.isEmpty()):
                # we need to allocate
                # to allocate use the relationship TLOAMLICINTDISTASSETWO
                licDistSet = licMbo.getMboSet("TLOAMLICINTDISTASSETWO")                
                licDistSet.reset()
                licDistSet.setWhere("assetnum='" + temasset + "'")
                
                # TLOAMLICINTDISTASSETWO relationship always return an empty set
                if (licDistSet.isEmpty()):
                    # use the siteid, orgid from the asset mbo
                    print "In SCCDLICDEC script: Allocating license " + licenseNum + " to asset " + temasset
                    licDistMbo = licDistSet.addAtEnd()
                    licDistMbo.setValue("licensenum", licenseNum)
                    licDistMbo.setValue("assetnum", temasset)
                    licDistMbo.setValue("targetobject","ASSET")
                    licDistMbo.setValue("capacity", 1)
                    licDistMbo.setValue("orgid",assetMbo.getString("ORGID"))
                    licDistMbo.setValue("siteid",assetMbo.getString("SITEID"))
                    licDistMbo.populateTrans()
                
                    worklogMbo.setValue("description", "Allocated license to TEM Client")
                    worklogMbo.setValue("clientviewable", 1)
                    worklogMbo.setValue("description_longdescription", "Allocated license " + licenseNum + " to asset "+temasset)
                    
                    
                    # add to SR Worklog
                    if (srWorklogMbo != None):
                        srWorklogMbo.setValue("description", getMsg("pmscoffering", "license_alloc_sum"))
                        srWorklogMbo.setValue("clientviewable", 1)
                        params = [ licenseNum, temasset]
                        srWorklogMbo.setValue("description_longdescription", getMsgWithParams("pmscoffering", "license_alloc_desc", params))
    
            else:
                print "License " + licenseNum + " is already allocated for asset " + temasset
                worklogMbo.setValue("description", "License already allocated to TEM Client")
                worklogMbo.setValue("clientviewable", 1)
                worklogMbo.setValue("description_longdescription", "License " + licenseNum + " is already allocated to asset " + temasset + ".\nSkipping allocation.")
                
                # add to SR Worklog
                if (srWorklogMbo != None):
                    srWorklogMbo.setValue("description", getMsg("pmscoffering", "license_already_alloc_sum"))
                    srWorklogMbo.setValue("clientviewable", 1)
                    params = [licenseNum, temasset]
                    srWorklogMbo.setValue("description_longdescription", getMsgWithParams("pmscoffering", "license_already_alloc_desc", params))