# AUTOSCRIPT NAME: EX2INVBAL
# CREATEDDATE: 2015-05-08 11:50:10
# CREATEDBY: UVX3
# CHANGEDATE: 2015-11-24 15:54:54
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.app.inventory import InvBalancesRemote
from java.util import Calendar
from java.util import Date

if not interactive and vphycount_modified:
 itmbo = mbo.reconcileBalances()
 if itmbo is not None:
  dt=Date()
  cal=Calendar.getInstance()
  cal.setTime(dt)
  cal.add(Calendar.SECOND, +5)
  itmbo.setValue("transdate", cal.getTime() , MboConstants.NOACCESSCHECK)
  itmbo.setValue("memo", "Auto Reconciliation", MboConstants.NOACCESSCHECK)
  itmbo.save()