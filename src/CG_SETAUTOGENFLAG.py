# AUTOSCRIPT NAME: CG_SETAUTOGENFLAG
# CREATEDDATE: 2012-04-25 12:51:28
# CREATEDBY: UHD0
# CHANGEDATE: 2012-04-25 14:32:08
# CHANGEBY: TRNADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants

priority = mbo.getInt("PRIORITY")
if priority>7:
    mbo.setValue("CG_AUTOGEN",1, MboConstants.NOACCESSCHECK)
else:
    mbo.setValue("CG_AUTOGEN",0, MboConstants.NOACCESSCHECK)