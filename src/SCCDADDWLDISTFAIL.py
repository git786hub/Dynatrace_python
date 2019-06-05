# AUTOSCRIPT NAME: SCCDADDWLDISTFAIL
# CREATEDDATE: 2012-12-07 10:38:20
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2012-12-07 13:57:11
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
#This Script adds a worklog entry to the related Service Request
# Input: 
#   None
# Outputs:
#   None
#
# Description
# Gets the related service request mbo from the parent workorder and adds a work log entry
# indicating that the software distribution failed.
#----------------------------------------------------------------------------------------------------
from psdi.server import MXServer

# this function returns the message for the given message key and message group
def getMsg(msgKey, msgGrp):
    msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgKey, msgGrp).getMessage()
    return msg


########################
####     main      ##### 
########################
# get the SR Worklog mboset
workorderSet = mbo.getMboSet("PARENTPROCESS")
workorder = workorderSet.getMbo(0)
originatingTicketSet = workorder.getMboSet("ORIGTICKET")
originatingTicket = originatingTicketSet.getMbo(0)
if (originatingTicket != None):
    srWorklogSet = originatingTicket.getMboSet("MODIFYWORKLOG")
    # add to SR Worklog
    srWorklogMbo = srWorklogSet.addAtEnd()
    srWorklogMbo.setValue("description", getMsg("pmscoffering", "invoke_tem_fail_sum"))
    srWorklogMbo.setValue("clientviewable", 1)
    srWorklogMbo.setValue("description_longdescription", getMsg("pmscoffering", "invoke_tem_fail_desc"))
    print "In SCCDADDWLDISTFAIL script: added an entry to SR worklog"