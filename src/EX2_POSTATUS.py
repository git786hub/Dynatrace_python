# AUTOSCRIPT NAME: EX2_POSTATUS
# CREATEDDATE: 2013-10-07 09:45:02
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:04:31
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

# set PO revision date/time based on status change to PROCESSED.
#
from java.util import Calendar
from java.util import Date
from psdi.mbo import MboConstants
 
if mbo.getString("status") == "PROCESSED":
    # Use the Calendar to get the current Date/Time
    c = Calendar.getInstance()
    c.add(Calendar.SECOND,0)

    # now set order date or revision date, depending on whether rev num is zero
    if mbo.getInt("revisionnum") == 0:
        mbo.setValue("ORDERDATE", c.getTime(),MboConstants.NOACCESSCHECK)
    else:
        mbo.setValue("EX2POREVDATE", c.getTime(),MboConstants.NOACCESSCHECK)