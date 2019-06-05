# AUTOSCRIPT NAME: EX2DISQPARVENDOR
# CREATEDDATE: 2014-03-26 08:49:02
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-10-13 20:15:43
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from java.util import Date
mbo.setValue("disabled", True)
mbo.setValue("ex2disableddate",Date())
mbo.setValueNull("ex2pendingdisableddate")

locset = mbo.getMboSet("companyparent")  # this really gets the children.  Really.
for i in range(locset.count()):
    locmbo = locset.getMbo(i)
    locmbo.setValue("disabled", True)
    locmbo.setValue("ex2disableddate",Date())
    locmbo.setValueNull("ex2pendingdisableddate")