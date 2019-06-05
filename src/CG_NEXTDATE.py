# AUTOSCRIPT NAME: CG_NEXTDATE
# CREATEDDATE: 2013-09-16 03:41:31
# CREATEDBY: UFDA
# CHANGEDATE: 2014-07-01 01:52:17
# CHANGEBY: UQRM
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from java.util import Date
#import java.util.Calendar
#import java.util.GregorianCalendar
from java.util import Calendar
from psdi.mbo import MboConstants

curdate = Date()
cal=Calendar.getInstance()
cal.setTime(curdate)

cal.add(Calendar.DATE, +1)
extdate =  cal.getTime()

print 'Current Date'
print curdate
print 'Extended date'
print extdate

mbo.setValue("NEXTDATE", extdate,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOACTION)