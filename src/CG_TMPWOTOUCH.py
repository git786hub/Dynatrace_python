# AUTOSCRIPT NAME: CG_TMPWOTOUCH
# CREATEDDATE: 2013-04-18 03:14:15
# CREATEDBY: UHD0
# CHANGEDATE: 2013-04-18 06:08:03
# CHANGEBY: UFCV
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.app.workorder import WORemote
from java.util import Calendar

print '############ CG_TMPWOTOUCH ############'

v_chngdate = mbo.getDate("CHANGEDATE")
print 'mbo.getDate:'
print v_chngdate

v_sec = v_chngdate.getSeconds()
print ' getseconds '
print v_sec

if v_sec == 59 : 
    v_sec = v_sec - 1
else :
    v_sec = v_sec + 1

print 'v_sec after set value:'
print v_sec

v_chngdate.setSeconds(v_sec)
print 'v_chngdate'
print v_chngdate
mbo.setValue("CHANGEDATE",v_chngdate,MboConstants.NOACCESSCHECK)
mbo.getThisMboSet().save()
v_chngdate2 = mbo.getDate("CHANGEDATE")
print 'mbo.getDate 2:'
print v_chngdate2