# AUTOSCRIPT NAME: EX2_CAPITEM
# CREATEDDATE: 2013-09-12 11:40:12
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-09-12 11:51:21
# CHANGEBY: UGL3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if mbo.getBoolean("CAPITALIZED") or mbo.getBoolean("ROTATING") :
    mbo.setValue("EX2LOWCOST",0,MboConstants.NOACCESSCHECK)
    mbo.setFieldFlag("EX2LOWCOST", MboConstants.READONLY, True)
else :
    mbo.setFieldFlag("EX2LOWCOST", MboConstants.READONLY, False)