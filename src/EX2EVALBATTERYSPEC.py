# AUTOSCRIPT NAME: EX2EVALBATTERYSPEC
# CREATEDDATE: 2018-10-11 06:17:16
# CREATEDBY: U4B0
# CHANGEDATE: 2019-02-07 22:57:30
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
if mbo.getString('ASSETATTRID') in ['FLOAT_V_TERMINAL', 'CHG_V','EQUAL_V_BAT','EQUAL_V_CHGR','SBIRB','BIRB','HIGH_CELL_RESIST','HIGH_TEMP','LOW_TEMP','BAT_V5MIN']:

 def getBatteryMbo(attribute):
  woBatterySet=mbo.getMboSet("$WORKORDERSPEC","WORKORDERSPEC", "wonum= '"+mbo.getString("WONUM") +"' and classstructureid = '"+mbo.getString("classstructureid")+"' and ASSETATTRID='"+attribute+"' and siteid='TRN'")
  woBatteryMbo=None
  if not woBatterySet.isEmpty():
   woBatteryMbo=woBatterySet.getMbo(0)
  return woBatteryMbo


 def setBatteryMbo(attribute, description,result,value):
  battspecSet= mbo.getMboSet("$CG_WORKORDERBATTERYSPEC","CG_WORKORDERBATTERYSPEC", "wonum= '"+mbo.getString("WONUM") +"' and classstructureid = '"+mbo.getString("classstructureid")+"' and ASSETATTRID='"+attribute+"' and siteid='TRN'")
  battspecMbo=None
  if result=='CAP':
   parentwoSet=mbo.getMboSet("$WORKORDER","WORKORDER", "wonum= '"+mbo.getString("WONUM") +"' and classstructureid = '"+mbo.getString("classstructureid")+"' and siteid='TRN'")
   if not parentwoSet.isEmpty():
    parentwoSet.getMbo(0).setValue("WOJO1", 'CAP', MboConstants.NOACCESSCHECK)
  if battspecSet.isEmpty():
   battspecMbo=battspecSet.add()
  else:
   battspecMbo=battspecSet.getMbo(0)
  battspecMbo.setValue("CLASSSTRUCTUREID", mbo.getString("CLASSSTRUCTUREID"))
  battspecMbo.setValue("SITEID", mbo.getString("SITEID"))
  battspecMbo.setValue("WONUM", mbo.getString("WONUM"))
  battspecMbo.setValue("ASSETATTRID", attribute)
  battspecMbo.setValue("DESCRIPTION", description)
  battspecMbo.setValue("RESULT", result)
  battspecMbo.setValue("NUMVALUE", value)
  #return batteryspecMbo
  battspecSet.save()
  if not battspecSet.isEmpty() and battspecMbo!=None:
   battspecSet.close()
 

 
 if mbo.getString('ASSETATTRID')=='HIGH_TEMP' and not mbo.isNull('NUMVALUE'):
   upper_value= mbo.getDouble('NUMVALUE')
   woBatteryMbo=getBatteryMbo('LOW_TEMP')
   if woBatteryMbo!=None and not woBatteryMbo.isNull('NUMVALUE'):
    lower_value= woBatteryMbo.getDouble('NUMVALUE')
    value= upper_value-lower_value
    if value>5 or value<-5:
     setBatteryMbo('HIGH_TEMP_LOW_TEMP', 'Temperature Difference', 'CAP',value)
    else:
     setBatteryMbo('HIGH_TEMP_LOW_TEMP', 'Temperature Difference', 'PASS',value) 

 elif mbo.getString('ASSETATTRID')=='LOW_TEMP' and not mbo.isNull('NUMVALUE'):
   lower_value= mbo.getDouble('NUMVALUE')
   woBatteryMbo=getBatteryMbo('HIGH_TEMP')
   if woBatteryMbo!=None and not woBatteryMbo.isNull('NUMVALUE'):
    upper_value= woBatteryMbo.getDouble('NUMVALUE')
    value= upper_value-lower_value
    if value>5 or value<-5:
     setBatteryMbo('HIGH_TEMP_LOW_TEMP', 'Temperature Difference', 'CAP',value)
    else:
     setBatteryMbo('HIGH_TEMP_LOW_TEMP', 'Temperature Difference', 'PASS',value)

 elif mbo.getString('ASSETATTRID')=='SBIRB' and not mbo.isNull('NUMVALUE'):
   upper_value=mbo.getDouble('NUMVALUE')
   if upper_value !=0:
    woBatteryMbo=getBatteryMbo('HIGH_CELL_RESIST')
    if woBatteryMbo and not woBatteryMbo.isNull('NUMVALUE'):
     lower_value= woBatteryMbo.getDouble('NUMVALUE')
     value= round((lower_value/upper_value)*100,2)
     if value>150:
      setBatteryMbo('PCT_BASELINE', 'Percentage of Baseline', 'CAP',value)
     else:
      setBatteryMbo('PCT_BASELINE', 'Percentage of Baseline', 'PASS',value)


 elif mbo.getString('ASSETATTRID')=='HIGH_CELL_RESIST' and not mbo.isNull('NUMVALUE'):
   lower_value=mbo.getDouble('NUMVALUE')
   woBatteryMbo=getBatteryMbo('SBIRB')
   if woBatteryMbo and not woBatteryMbo.isNull('NUMVALUE'):
    upper_value= woBatteryMbo.getDouble('NUMVALUE')
    if upper_value !=0:
     value=  round((lower_value/upper_value)*100,2)
     if value>150:
      setBatteryMbo('PCT_BASELINE', 'Percentage of Baseline', 'CAP',value)
     else:
      setBatteryMbo('PCT_BASELINE', 'Percentage of Baseline', 'PASS',value)

 #Added as part of ITO-107460

 elif mbo.getString('ASSETATTRID')=='BIRB' and not mbo.isNull('NUMVALUE'):
   upper_value=mbo.getDouble('NUMVALUE')
   if upper_value !=0:
    woBatteryMbo=getBatteryMbo('HIGH_CELL_RESIST')
    if woBatteryMbo and not woBatteryMbo.isNull('NUMVALUE'):
     lower_value= woBatteryMbo.getDouble('NUMVALUE')
     value= round((lower_value/upper_value)*100,2)
     if value>150:
      setBatteryMbo('PCT_BASELINE', 'Percentage of Baseline', 'CAP',value)
     else:
      setBatteryMbo('PCT_BASELINE', 'Percentage of Baseline', 'PASS',value)

 elif mbo.getString('ASSETATTRID')=='HIGH_CELL_RESIST' and not mbo.isNull('NUMVALUE'):
   lower_value=mbo.getDouble('NUMVALUE')
   woBatteryMbo=getBatteryMbo('BIRB')
   if woBatteryMbo and not woBatteryMbo.isNull('NUMVALUE'):
    upper_value= woBatteryMbo.getDouble('NUMVALUE')
    if upper_value !=0:
     value=  round((lower_value/upper_value)*100,2)
     if value>150:
      setBatteryMbo('PCT_BASELINE', 'Percentage of Baseline', 'CAP',value)
     else:
      setBatteryMbo('PCT_BASELINE', 'Percentage of Baseline', 'PASS',value)


 elif mbo.getString('ASSETATTRID')=='FLOAT_V_TERMINAL' and not mbo.isNull('NUMVALUE'):
   upper_value= mbo.getDouble('NUMVALUE')
   woBatteryMbo=getBatteryMbo('CHG_V')
   if woBatteryMbo and not woBatteryMbo.isNull('NUMVALUE'):
    lower_value= woBatteryMbo.getDouble('NUMVALUE')
    value= upper_value-lower_value
    if upper_value>60 or upper_value==60:
     if (value>1 or value<-1):
      setBatteryMbo('FLOAT_V_TERMINAL_BAT_V', 'Voltage Difference at Battery Terminal', 'CAP',value)
     else:
      setBatteryMbo('FLOAT_V_TERMINAL_BAT_V', 'Voltage Difference at Battery Terminal', 'PASS',value)
    elif upper_value<60:
     if (value>0.5 or value<-0.5):
      setBatteryMbo('FLOAT_V_TERMINAL_BAT_V', 'Voltage Difference at Battery Terminal', 'CAP',value)
     else:
      setBatteryMbo('FLOAT_V_TERMINAL_BAT_V', 'Voltage Difference at Battery Terminal', 'PASS',value)

 elif mbo.getString('ASSETATTRID')=='CHG_V' and not mbo.isNull('NUMVALUE'):
   lower_value= mbo.getDouble('NUMVALUE')
   woBatteryMbo=getBatteryMbo('FLOAT_V_TERMINAL')
   if woBatteryMbo and not woBatteryMbo.isNull('NUMVALUE'):
    upper_value= woBatteryMbo.getDouble('NUMVALUE')
    value= upper_value-lower_value
    if upper_value>60 or upper_value==60:
     if (value>1 or value<-1):
      setBatteryMbo('FLOAT_V_TERMINAL_BAT_V', 'Voltage Difference at Battery Terminal', 'CAP',value)
     else:
      setBatteryMbo('FLOAT_V_TERMINAL_BAT_V', 'Voltage Difference at Battery Terminal', 'PASS',value)
    elif upper_value<60:
     if (value>0.5 or value<-0.5):
      setBatteryMbo('FLOAT_V_TERMINAL_BAT_V', 'Voltage Difference at Battery Terminal', 'CAP',value)
     else:
      setBatteryMbo('FLOAT_V_TERMINAL_BAT_V', 'Voltage Difference at Battery Terminal', 'PASS',value)

 elif mbo.getString('ASSETATTRID')=='EQUAL_V_BAT' and not mbo.isNull('NUMVALUE'):
   upper_value= mbo.getDouble('NUMVALUE')
   woBatteryMbo=getBatteryMbo('EQUAL_V_CHGR')
   if woBatteryMbo and not woBatteryMbo.isNull('NUMVALUE'):
    lower_value= woBatteryMbo.getDouble('NUMVALUE')
    value= upper_value-lower_value
    if upper_value>60 or upper_value==60:
     if (value>1 or value<-1):
      setBatteryMbo('EQUAL_V_BAT_EQUAL_V_CHGR', 'Equalized Voltage Difference at Battery Terminal', 'CAP',value)
     else:
      setBatteryMbo('EQUAL_V_BAT_EQUAL_V_CHGR', 'Equalized Voltage Difference at Battery Terminal', 'PASS',value)
    elif upper_value<60:
     if (value>1 or value<-1):
      setBatteryMbo('EQUAL_V_BAT_EQUAL_V_CHGR', 'Equalized Voltage Difference at Battery Terminal', 'CAP',value)
     else:
      setBatteryMbo('EQUAL_V_BAT_EQUAL_V_CHGR', 'Equalized Voltage Difference at Battery Terminal', 'PASS',value)

 elif mbo.getString('ASSETATTRID')=='EQUAL_V_CHGR' and not mbo.isNull('NUMVALUE'):
   lower_value= mbo.getDouble('NUMVALUE')
   woBatteryMbo=getBatteryMbo('EQUAL_V_BAT')
   if woBatteryMbo and not woBatteryMbo.isNull('NUMVALUE'):
    upper_value= woBatteryMbo.getDouble('NUMVALUE')
    value= upper_value-lower_value
    if upper_value>60 or upper_value==60:
     if (value>1 or value<-1):
      setBatteryMbo('EQUAL_V_BAT_EQUAL_V_CHGR', 'Equalized Voltage Difference at Battery Terminal', 'CAP',value)
     else:
      setBatteryMbo('EQUAL_V_BAT_EQUAL_V_CHGR', 'Equalized Voltage Difference at Battery Terminal', 'PASS',value)
    elif upper_value<60:
     if (value>0.5 or value<-0.5):
      setBatteryMbo('EQUAL_V_BAT_EQUAL_V_CHGR', 'Equalized Voltage Difference at Battery Terminal', 'CAP',value)
     else:
      setBatteryMbo('EQUAL_V_BAT_EQUAL_V_CHGR', 'Equalized Voltage Difference at Battery Terminal', 'PASS',value)

#New requirement formula added for BAT_V5MIN-ITO-105348

 elif mbo.getString('ASSETATTRID')=='BAT_V5MIN' and not mbo.isNull('NUMVALUE'):
    value= mbo.getDouble('NUMVALUE')
    if value<60 :
     if (value<47.2 or value==47.2):
      setBatteryMbo('BAT_V5MIN', 'Voltage Reading after 5 min', 'CAP',value)
     else:
      setBatteryMbo('BAT_V5MIN', 'Voltage Reading after 5 min', 'PASS',value)
    elif value>60:
      if (value<117 or value==117):
       setBatteryMbo('BAT_V5MIN', 'Voltage Reading after 5 min', 'CAP',value)
      else:
       setBatteryMbo('BAT_V5MIN', 'Voltage Reading after 5 min', 'PASS',value)


batteryspecresSet=mbo.getMboSet("$CG_WORKORDERBATTERYSPEC","CG_WORKORDERBATTERYSPEC", "wonum= '"+mbo.getString("WONUM") +"' and classstructureid = '"+mbo.getString("classstructureid")+"' and siteid='TRN'")

if not batteryspecresSet.isEmpty():
 batteryspecresMbo= batteryspecresSet.moveFirst()
 isCAP= False

 while batteryspecresMbo != None:
  if batteryspecresMbo.getString('RESULT')=='CAP':
   isCAP=True
   break;
  batteryspecresMbo=batteryspecresSet.moveNext()

parentworesSet=mbo.getMboSet("$WORKORDER","WORKORDER", "wonum= '"+mbo.getString("WONUM") +"' and classstructureid = '"+mbo.getString("classstructureid")+"' and siteid='TRN'")

if isCAP:
 if not parentworesSet.isEmpty():
  parentworesSet.getMbo(0).setValue("WOJO1", 'CAP', MboConstants.NOACCESSCHECK)
else:
 if not parentworesSet.isEmpty():
  parentworesSet.getMbo(0).setValue("WOJO1", 'PASS', MboConstants.NOACCESSCHECK)


#Added extracode to add values in custom table
woBatterydefSet=mbo.getMboSet("$WORKORDERSPEC","WORKORDERSPEC", "wonum= '"+mbo.getString("WONUM") +"' and classstructureid = '"+mbo.getString("classstructureid")+"' and siteid='TRN'")
woBatterydefMbo=None
if not woBatterydefSet.isEmpty():
 woBatterydefMbo= woBatterydefSet.moveFirst()
while woBatterydefMbo != None:
 if woBatterydefMbo.getString('ASSETATTRID') in ['GENERAL_COND', 'CELL_NUM', 'CASE_CRACK', 'INSPECT_TERMINAL', 'RACK_DETERIATION', 'RACK_FASTENER', 'CELL_VENT', 'PLATE_SULFATING', 'PLATE_COLOR', 'PLATE_CONNECT', 'SEALS_DISTORTION', 'PLATE_DISTORTION', 'POST_GROWTH', 'JAR_DISTORTION']:
  battspecdefSet= mbo.getMboSet("$CG_WORKORDERBATTERYSPEC","CG_WORKORDERBATTERYSPEC", "wonum= '"+woBatterydefMbo.getString("WONUM") +"' and classstructureid = '"+woBatterydefMbo.getString("classstructureid")+"' and ASSETATTRID='"+woBatterydefMbo.getString("ASSETATTRID")+"' and siteid='TRN'")
  battspecdefMbo=None
  if battspecdefSet.isEmpty():
   battspecdefMbo=battspecdefSet.add()
  else:
   battspecdefMbo=battspecdefSet.getMbo(0)
  battspecdefMbo.setValue("CLASSSTRUCTUREID",woBatterydefMbo.getString("CLASSSTRUCTUREID"))
  battspecdefMbo.setValue("SITEID", woBatterydefMbo.getString("SITEID"))
  battspecdefMbo.setValue("WONUM", woBatterydefMbo.getString("WONUM"))
  battspecdefMbo.setValue("ASSETATTRID", woBatterydefMbo.getString("ASSETATTRID"))
  battspecdefMbo.setValue("DESCRIPTION", woBatterydefMbo.getMboSet("ASSETATTRIBUTE").getMbo(0).getString("DESCRIPTION"))
  battspecdefMbo.setValue("RESULT", woBatterydefMbo.getString("ALNVALUE"))
  battspecdefMbo.setValue("ALNVALUE", woBatterydefMbo.getString("ALNVALUE"))
   #return batteryspecMbo
  battspecdefSet.save()
  if not battspecdefSet.isEmpty() and battspecdefMbo!=None:
   battspecdefSet.close()
 woBatterydefMbo=woBatterydefSet.moveNext()