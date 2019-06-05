# AUTOSCRIPT NAME: CG_SETLABORCHANGE
# CREATEDDATE: 2012-07-15 14:55:07
# CREATEDBY: UHD0
# CHANGEDATE: 2012-12-01 15:42:31
# CHANGEBY: UWUD
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

if mbo.getString("CG_MULTIVEHICLE.SETPRIMARYFLAG") == "Yes" and mbo.getString("TRANSTYPE") == "WORK" :
    mbo.setValue("CG_PRIVEHICLE",True,MboConstants.NOACCESSCHECK)
else:
    mbo.setValue("CG_PRIVEHICLE",False,MboConstants.NOACCESSCHECK)

mbo.setValueNull("CG_MEALS", MboConstants.NOACCESSCHECK)