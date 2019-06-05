# AUTOSCRIPT NAME: EX2_COPYPR2LINE
# CREATEDDATE: 2013-09-25 14:34:15
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-02-19 13:39:28
# CHANGEBY: UUYZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

# Populate custom PRLine fields from PR header

from psdi.mbo import MboConstants 

if interactive and onadd:

    prmbo = mbo.getOwner()
    mbo.setValue("EX2PROJECT",prmbo.getString("EX2PROJECT"),MboConstants.NOACCESSCHECK)
    mbo.setValue("EX2TASKSOW",prmbo.getString("EX2TASKSOW"),MboConstants.NOACCESSCHECK)
    mbo.setValue("EX2DROPSHIP",prmbo.getString("EX2DROPSHIP"),MboConstants.NOACCESSCHECK)
    mbo.setValue("EX2INVAPPR",prmbo.getString("EX2INVAPPR"),MboConstants.NOACCESSCHECK)