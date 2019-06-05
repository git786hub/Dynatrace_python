# AUTOSCRIPT NAME: EX2_VMI
# CREATEDDATE: 2013-09-07 10:47:57
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-09-08 09:20:24
# CHANGEBY: UGL3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if mbo.getBoolean("EX2VMI") :
    mbo.setValue("REORDER",0,MboConstants.NOACCESSCHECK)
    mbo.setFieldFlag("REORDER", MboConstants.READONLY, True)
    mbo.setFieldFlag("VENDOR", MboConstants.REQUIRED, True)
else :
    mbo.setFieldFlag("VENDOR", MboConstants.REQUIRED, False)
    mbo.setFieldFlag("REORDER", MboConstants.READONLY, False)