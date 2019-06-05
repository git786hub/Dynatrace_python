# AUTOSCRIPT NAME: CG_PLUSPWOPRICETOTALS
# CREATEDDATE: 2013-09-19 06:11:59
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-09-19 06:11:59
# CHANGEBY: UM7V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

estmatprice = mbo.getString("CG_ESTMATPRICE")
if estmatprice == '':
   mbo.setValue("CG_ESTMATPRICE",0,MboConstants.NOACCESSCHECK)