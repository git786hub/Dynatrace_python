# AUTOSCRIPT NAME: CG_TIME
# CREATEDDATE: 2012-04-11 12:38:36
# CREATEDBY: UHD0
# CHANGEDATE: 2013-05-14 03:22:52
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

import java.util.Calendar

time = mbo.getDate(launchPoint)
remainder = time.getMinutes() % 15
    
if remainder == 0 or time.getMinutes() == 0:
  time.setMinutes((time.getMinutes() / 15) * 15)
  mbo.setValue(launchPoint, time)
else:
  time.setMinutes(((time.getMinutes() / 15)+1) * 15)
  mbo.setValue(launchPoint, time)