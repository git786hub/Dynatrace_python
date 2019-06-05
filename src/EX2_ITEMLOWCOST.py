# AUTOSCRIPT NAME: EX2_ITEMLOWCOST
# CREATEDDATE: 2013-09-12 11:15:37
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-09-12 11:20:57
# CHANGEBY: UGL3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if mbo.getBoolean("EX2LOWCOST") :
    mbo.setValue("CAPITALIZED",0,MboConstants.NOACCESSCHECK)
    mbo.setValue("ROTATING",0,MboConstants.NOACCESSCHECK)
    mbo.setFieldFlag("ROTATING", MboConstants.READONLY, True)
    mbo.setFieldFlag("CAPITALIZED", MboConstants.READONLY, True)
else :
    mbo.setFieldFlag("ROTATING", MboConstants.READONLY, False)
    mbo.setFieldFlag("CAPITALIZED", MboConstants.READONLY, False)