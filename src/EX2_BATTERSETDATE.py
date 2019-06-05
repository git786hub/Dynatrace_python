# AUTOSCRIPT NAME: EX2_BATTERSETDATE
# CREATEDDATE: 2018-09-11 12:32:36
# CREATEDBY: U4B0
# CHANGEDATE: 2018-11-06 11:36:58
# CHANGEBY: U4B0
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from java.util import Date
from java.util import Calendar
from java.text import SimpleDateFormat


today= SimpleDateFormat("dd-MMM-yy").format(Date())
mbo.setValue("alnvalue",today,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)