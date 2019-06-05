# AUTOSCRIPT NAME: EX2_ROTATINGITEM
# CREATEDDATE: 2013-09-12 11:33:17
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-09-12 11:49:05
# CHANGEBY: UGL3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if mbo.getBoolean("ROTATING") or mbo.getBoolean("CAPITALIZED"):
    mbo.setValue("EX2LOWCOST",0,MboConstants.NOACCESSCHECK)
    mbo.setFieldFlag("EX2LOWCOST", MboConstants.READONLY, True)
else :
    mbo.setFieldFlag("EX2LOWCOST", MboConstants.READONLY, False)