# AUTOSCRIPT NAME: EX2PRWKLOG
# CREATEDDATE: 2013-10-01 15:03:16
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-10-01 15:09:31
# CHANGEBY: UUYZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if not onadd:
    mbo.setFieldFlag("EX2DESCRIPTION", MboConstants.READONLY, True)
    mbo.setFieldFlag("EX2DESCRIPTION_LONGDESCRIPTION", MboConstants.READONLY, True)