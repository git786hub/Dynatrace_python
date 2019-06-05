# AUTOSCRIPT NAME: EX2_CONTRACTNOTIFICATION
# CREATEDDATE: 2015-05-03 05:15:16
# CREATEDBY: UVX3
# CHANGEDATE: 2015-05-03 05:15:16
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote

# If enddate has been changed reset the notification flag
if  ENDDATE != EX2ENDDATE:
    mbo.setValue("EX2EMAILFLAG", '0',MboConstants.NOACCESSCHECK)
    mbo.setValue("EX2ENDDATE", ENDDATE ,MboConstants.NOACCESSCHECK)