# AUTOSCRIPT NAME: EX2WOBATTERYSPEC
# CREATEDDATE: 2018-09-27 15:38:45
# CREATEDBY: U4B0
# CHANGEDATE: 2019-02-07 22:58:19
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
def addmodifyBatteryMbo(attribute, alnvalue,numvalue,result):
 batteryspecSet= mbo.getMboSet("$CG_WORKORDERBATTERYSPEC","CG_WORKORDERBATTERYSPEC", "wonum= '"+mbo.getString("WONUM") +"' and classstructureid = '"+mbo.getString("classstructureid")+"' and ASSETATTRID='"+attribute+"' and siteid='TRN'")
 batteryMbo=None
 if result=='CAP':
  parentwoSet=mbo.getMboSet("$WORKORDER","WORKORDER", "wonum= '"+mbo.getString("WONUM") +"' and classstructureid = '"+mbo.getString("classstructureid")+"' and siteid='TRN'")
  if not parentwoSet.isEmpty():
   parentwoSet.getMbo(0).setValue("WOJO1", 'CAP', MboConstants.NOACCESSCHECK)
   
 if batteryspecSet.isEmpty():
  batteryMbo=batteryspecSet.add()
 else:
  batteryMbo=batteryspecSet.getMbo(0)
 batteryMbo.setValue("CLASSSTRUCTUREID", mbo.getString("CLASSSTRUCTUREID"))
 batteryMbo.setValue("SITEID", mbo.getString("SITEID"))
 batteryMbo.setValue("WONUM", mbo.getString("WONUM"))
 batteryMbo.setValue("ASSETATTRID", attribute)
 batteryMbo.setValue("DESCRIPTION", mbo.getMboSet("ASSETATTRIBUTE").getMbo(0).getString("DESCRIPTION"))
 batteryMbo.setValue("ALNVALUE", alnvalue)
 batteryMbo.setValue("RESULT", result)
 batteryMbo.setValue("NUMVALUE", numvalue)
 batteryspecSet.save()
 if not batteryspecSet.isEmpty() and batteryMbo!=None:
   batteryspecSet.close()


if mbo.getString('ASSETATTRID') in ['GENERAL_COND', 'CELL_NUM', 'CASE_CRACK', 'INSPECT_TERMINAL', 'RACK_DETERIATION', 'RACK_FASTENER', 'CELL_VENT', 'PLATE_SULFATING', 'PLATE_COLOR', 'PLATE_CONNECT', 'SEALS_DISTORTION', 'PLATE_DISTORTION', 'POST_GROWTH', 'JAR_DISTORTION']:
 if not mbo.isNull("ALNVALUE"):
  batteryspecMbo= addmodifyBatteryMbo(mbo.getString('ASSETATTRID'), mbo.getString("ALNVALUE"),'' , mbo.getString("ALNVALUE"))
  mbo.setFieldFlag("ALNVALUE", MboConstants.REQUIRED, True)

elif mbo.getString('ASSETATTRID') in ['FLOAT_V_TERMINAL','BAT_V5MIN','CHG_INSTA','CHG_CRNT',  'CHG_V','EQUAL_V_BAT','EQUAL_V_CHGR','SBIRB','BIRB','HIGH_CELL_RESIST','HIGH_TEMP','LOW_TEMP']:
 if not mbo.isNull("NUMVALUE"):
  value=mbo.getDouble("NUMVALUE")
  if mbo.getString('ASSETATTRID') in ['FLOAT_V_TERMINAL', 'CHG_V','EQUAL_V_BAT','EQUAL_V_CHGR','BAT_V5MIN','CHG_INSTA','CHG_CRNT',]:
   value=round(value,1)
   mbo.setValue('NUMVALUE', value)
  elif mbo.getString('ASSETATTRID') in ['SBIRB','BIRB','HIGH_CELL_RESIST']:
   value=round(value,0)
   mbo.setValue('NUMVALUE', value)
  batteryspecMbo= addmodifyBatteryMbo(mbo.getString('ASSETATTRID'), '',value, '')
  #batteryspecMbo.setValue("NUMVALUE", mbo.getDouble("NUMVALUE"))

elif mbo.getString('ASSETATTRID') in ['FLOAT_RIPPLE','EQUAL_RIPPLE']:
 if not mbo.isNull("NUMVALUE"):
  value= mbo.getDouble("NUMVALUE")
  if value>5 or value<-5:
   batteryspecMbo= addmodifyBatteryMbo(mbo.getString('ASSETATTRID'),'', mbo.getDouble("NUMVALUE"),'CAP')
  else:
   batteryspecMbo= addmodifyBatteryMbo(mbo.getString('ASSETATTRID'), '',mbo.getDouble("NUMVALUE"),'PASS')