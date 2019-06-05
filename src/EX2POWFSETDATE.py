# AUTOSCRIPT NAME: EX2POWFSETDATE
# CREATEDDATE: 2015-07-17 01:28:21
# CREATEDBY: U047
# CHANGEDATE: 2016-02-15 04:39:47
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from java.util import Date
from java.util import Calendar

sysdate=Date()
cal=Calendar.getInstance()
cal.setTime(sysdate)
day =cal.get(Calendar.DAY_OF_WEEK)
cal.add(Calendar.DATE,+4)
duedate=cal.getTime()
print '-----------------------------------due date-------------------------------------'
print duedate
print '-----------------------------------due date---weekday----------------------------------'
print cal.get(Calendar.DAY_OF_WEEK)
ex2powf = mbo.getMboSet("EX2ASSIGNEE")
count=ex2powf.count()
if count>0 :
	mbo1 = ex2powf.getMbo(0)
	mbo1.setValue("ex2assigndate",sysdate,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
        mbo1.setValue("ex2duedate",duedate, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)