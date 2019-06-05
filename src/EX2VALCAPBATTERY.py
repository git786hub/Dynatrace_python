# AUTOSCRIPT NAME: EX2VALCAPBATTERY
# CREATEDDATE: 2018-09-28 00:36:04
# CREATEDBY: U4B0
# CHANGEDATE: 2019-02-07 22:57:54
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
batteryspecSet=mbo.getMboSet("$CG_WORKORDERBATTERYSPEC","CG_WORKORDERBATTERYSPEC", "wonum= '"+mbo.getString("WONUM") +"' and classstructureid = '"+mbo.getString("classstructureid")+"' and siteid='TRN'")

if not batteryspecSet.isEmpty():
 batteryspecMbo= batteryspecSet.moveFirst()
 isCAP= False

 while batteryspecMbo != None:
  if batteryspecMbo.getString('RESULT')=='CAP':
   isCAP=True
   break;
  batteryspecMbo=batteryspecSet.moveNext()

 if isCAP:
  mbo.setValue("WOJO1", 'CAP', MboConstants.NOACCESSCHECK )
 else:
  mbo.setValue("WOJO1", 'PASS', MboConstants.NOACCESSCHECK)