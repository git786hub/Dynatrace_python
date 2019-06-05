# AUTOSCRIPT NAME: CG_SITE_POPULATE
# CREATEDDATE: 2015-01-29 07:35:59
# CREATEDBY: USZN
# CHANGEDATE: 2015-04-02 11:49:12
# CHANGEBY: UQRM
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from java.util import Date
#import java.util.Calendar
#import java.util.GregorianCalendar
from java.util import Calendar

#mbo.setValue("EX2CHANGEDATE",Date())
#mbosetattrid = mbo.getMboSet("ASSETATTRIBUTE")

#serialnum = mbo.getString("SERIALNUM")
#if serialnum is not None and serialnum <> "" :
#   mbo.setValue("EQ2", mbo.getString("SITEID"),MboConstants.NOACCESSCHECK)


curdate = Date()

mbo.setValue("EQ6", curdate ,MboConstants.NOACCESSCHECK)