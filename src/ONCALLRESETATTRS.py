# AUTOSCRIPT NAME: ONCALLRESETATTRS
# CREATEDDATE: 2012-08-13 15:24:41
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2012-09-18 17:34:40
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import Mbo

# This script clears the value of the attributes, ONCALLFIRSTROTASSNPERSON
# and ONCALLSTARTTIME, on the incident object when the incident status changes 
# from QUEUED to any other state. This takes onCallFirstRotAssnPerson and 
# onCallStartTime as the OUTPUT parameters

#get the translated value of the QUEUED status
statusListName = mbo.getStatusListName()
queueStatus =   mbo.getTranslator().toExternalDefaultValue(statusListName, "QUEUED")	

#status_previous refers to the previous value of the status attribute
#i.e. the value just before it was changed. 
if (status_previous == queueStatus):
    onCallFirstRotAssnPerson =  None
    onCallStartTime = None