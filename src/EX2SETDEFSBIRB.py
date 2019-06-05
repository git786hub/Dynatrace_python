# AUTOSCRIPT NAME: EX2SETDEFSBIRB
# CREATEDDATE: 2018-09-28 00:39:31
# CREATEDBY: U4B0
# CHANGEDATE: 2019-02-07 22:59:18
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

if (mbo.getThisMboSet().getParentApp()== 'WOT_TRN') :
 #if launchPoint=='EX2SETDEFSBIRB':
  if mbo.getString('CLASSSTRUCTUREID') in ['3039', '3041'] and mbo.getString('ASSETATTRID') in ['SBIRB','BIRB'] and mbo.isNull('NUMVALUE'):
   mbo.setValue("NUMVALUE", 0)