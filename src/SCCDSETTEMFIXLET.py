# AUTOSCRIPT NAME: SCCDSETTEMFIXLET
# CREATEDDATE: 2012-10-15 17:10:25
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2015-05-19 05:46:54
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
# ***************************** End Standard Header ****************************
#==============================================================================

#-----------------------------------------------------------------------------
#This Script Sets the FixletID and SiteID from the Item in the Plans Section
# Input: 
#   None
# Outputs:
#    temfixletid         - task Id of the Tivoli Endpoint Manager Server
#    temfixletsiteid     - site Id of the fixlet
#    temendpoint         - name of the maximo end point containing TEM server credential     
#
# Description
# This script gets the task ID, siteID and end point name from the deployable software and 
# sets the specification attributes of the WOACTIVITY. These specification attributes are parameters to 
# the automation script. These values are used by the other autoscripts invoking the action on 
# TEM Server and querying the status of an action.   
#
#----------------------------------------------------------------------------------------------------

from psdi.server import MXServer

# this function returns the message for the given message key and message group
def getMsg(msgKey, msgGrp):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgKey, msgGrp).getMessage()
    return msg


########################
####     main      ##### 
########################
returncode = "0"

# add a worklog entry to SR to indicate license is reserved
workorderSet = mbo.getMboSet("PARENTPROCESS")
workorder = workorderSet.getMbo(0)
worklogSet = mbo.getMboSet("MODIFYWORKLOG")
worklogMbo = worklogSet.addAtEnd()
worklogMbo .setValue("description", getMsg("pmscoffering", "license_reserved_sum"))
worklogMbo .setValue("clientviewable", 1)
worklogMbo .setValue("description_longdescription", getMsg("pmscoffering", "license_reserved_desc"))

originatingTicketSet = workorder.getMboSet("ORIGTICKET")
originatingTicket = originatingTicketSet.getMbo(0)
if (originatingTicket != None):
    srWorklogSet = originatingTicket.getMboSet("MODIFYWORKLOG")
    # add to SR Worklog
    srWorklogMbo = srWorklogSet.addAtEnd()
    srWorklogMbo.setValue("description", getMsg("pmscoffering", "license_reserved_sum"))
    srWorklogMbo.setValue("clientviewable", 1)
    srWorklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "license_reserved_desc"))


wpItemSet = mbo.getMboSet("WPITEM")

wpItem = wpItemSet.getMbo(0)
if (wpItem != None):   
    wpitemnum = wpItem.getString("ITEMNUM")
    wpitemsetid = wpItem.getString("ITEMSETID")
   
    sqlToFindItem = "itemnum='" + wpitemnum + "' and itemsetid='" + wpitemsetid + "'"
    print "\n In SCCDSETTEMFIXLET script: ", sqlToFindItem, "\n"
    itemSet = wpItem.getMboSet("$ITEM", "item", sqlToFindItem) 
    
    item = itemSet.getMbo(0)
    if (item == None):        
        print "In SCCDSETTEMFIXLET script: No item found for the itemnum :  " + wpitemnum + " itemsetid:  " + wpitemsetid
        print "In SCCDSETTEMFIXLET script: Check if an item is associated with the job plan under Materials tab"
        worklogMbo = worklogSet.addAtEnd()
        worklogMbo.setValue("description", "No item found")
        worklogMbo.setValue("clientviewable", 1)
        worklogMbo.setValue("description_longdescription",  "No item found for the itemnum :  " + wpitemnum + " itemsetid:  " + wpitemsetid) 
    else:         
        softwareSet = item.getMboSet("TLOAMSOFTWARE")
        software = softwareSet.getMbo(0)
        if (software == None):
            print "In SCCDSETTEMFIXLET script: No software found for item: " + wpitemnum 
            worklogSet = mbo.getMboSet("MODIFYWORKLOG")
            worklogMbo = worklogSet.addAtEnd()
            worklogMbo.setValue("description", "No software found")
            worklogMbo.setValue("clientviewable", 1)
            worklogMbo.setValue("description_longdescription", "Check to make sure that the deployable software has the TEM taskID as specified in the instructions") 
        else:            
            deployableSoftwareSet = software.getMboSet("TAMITDEPLOYSWTASK")
            
            # This is the place to make changes to handle the case where more than one task 
            # exists for a given software package
            
            deployableSoftware = deployableSoftwareSet.getMbo(0)
            if (deployableSoftware != None):                
                fixletID = deployableSoftware.getString("TASKID")
                siteID = deployableSoftware.getString("SITEID")  
                endPointName = deployableSoftware.getString("ENDPOINTNAME")               
                    
                print "In SCCDSETTEMFIXLET script: fixletID: ", fixletID
                print "In SCCDSETTEMFIXLET script: fixletSiteID: ", siteID
                print "In SCCDSETTEMFIXLET script: endPointName = ", endPointName
                               
                if (endPointName == None or endPointName == ''):
                    # default to IEMSWDSERVER
                    endPointName = "IEMSWDSERVER"
                    print "In SCCDSETTEMFIXLET script: defaulting to IEMSWDSERVER end point"
                                  
                temfixletid = fixletID
                temfixletsiteid = siteID
                temendpoint = endPointName
                if (temfixletid == None):
                    worklogSet = mbo.getMboSet("MODIFYWORKLOG")
                    worklogMbo = worklogSet.addAtEnd()
                    worklogMbo.setValue("description", "No Task ID Found")
                    worklogMbo.setValue("clientviewable", 1)
                    worklogMbo.setValue("description_longdescription", "Check to make sure that the deployable software has the TEM taskID as specified in the instructions")                
                
            else:
                worklogSet = mbo.getMboSet("MODIFYWORKLOG")
                worklogMbo = worklogSet.addAtEnd()
                worklogMbo.setValue("description", "Failed: No Deployable Software Found")
                worklogMbo.setValue("clientviewable", 1)
                worklogMbo.setValue("description_longdescription", "The specified software product does not exist.")                
                
else:
    print "In SCCDSETTEMFIXLET script: No item specified. Check to make sure that an item is associated with job plan"
    worklogSet = mbo.getMboSet("MODIFYWORKLOG")
    worklogMbo = worklogSet.addAtEnd()
    worklogMbo.setValue("description", "Failed: No item found")
    worklogMbo.setValue("clientviewable", 1)
    worklogMbo.setValue("description_longdescription", "Check to make sure that an item is associated with the job plan")