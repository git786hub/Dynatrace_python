# AUTOSCRIPT NAME: CG_GETDFTMETERREADDATE
# CREATEDDATE: 2012-07-23 19:40:41
# CREATEDBY: UHD0
# CHANGEDATE: 2015-06-18 08:45:48
# CHANGEBY: UW1X
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.app.workorder import WORemote
from java.util import Date

ownermbo= mbo.getOwner()
parentwombo = ownermbo.getOwner()

if parentwombo and isinstance(parentwombo,WORemote) and parentwombo.getString("CG_DEFAULTREADINGDATE") <>""  and parentwombo.getString("CG_DEFAULTREADINGDATE") is not None:
 if parentwombo and isinstance(parentwombo,WORemote) and mbo.getString("newreading") is not None and mbo.getString("newreading")  <> "" :
    newreaddate = parentwombo.getDate("CG_DEFAULTREADINGDATE")
    mbo.setValue("inspector",parentwombo.getUserInfo().getPersonId(),MboConstants.NOACCESSCHECK)
 else :
    mbo.setValueNull("NEWREADINGDATE",MboConstants.NOACCESSCHECK)
    mbo.setValueNull("inspector",MboConstants.NOACCESSCHECK)

else :
 if parentwombo and isinstance(parentwombo,WORemote) and mbo.getString("newreading") is not None and mbo.getString("newreading")  <> "" :
    mbo.setValue("inspector",parentwombo.getUserInfo().getPersonId(),MboConstants.NOACCESSCHECK)