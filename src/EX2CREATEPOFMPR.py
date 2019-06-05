# AUTOSCRIPT NAME: EX2CREATEPOFMPR
# CREATEDDATE: 2013-09-30 13:18:02
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-02-06 08:30:34
# CHANGEBY: UUYC
# SCRIPTLANGUAGE: jython
# STATUS: Active

# Create a PO based on the PR - called as an escalation action
#
from java.util import Calendar
from java.util import Date
from psdi.mbo import MboConstants
 
# Use the Calendar to get the current Date/Time
c = Calendar.getInstance()
c.add(Calendar.SECOND,0)
mbo.createPOsFromPR(c.getTime())