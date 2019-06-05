# AUTOSCRIPT NAME: CG_LABVEHOBJ
# CREATEDDATE: 2012-06-01 08:58:26
# CREATEDBY: UHD0
# CHANGEDATE: 2012-06-01 09:09:48
# CHANGEBY: UTWF
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

mCount = mbo.getThisMboSet().count()

if mCount == 0:
    mbo.setValue("SETPRIMARYFLAG", "Yes", MboConstants.NOACCESSCHECK)