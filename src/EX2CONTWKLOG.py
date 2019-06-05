# AUTOSCRIPT NAME: EX2CONTWKLOG
# CREATEDDATE: 2013-10-16 16:34:54
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-10-16 16:38:49
# CHANGEBY: UUYZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if not onadd:
    mbo.setFieldFlag("EX2DESCRIPTION", MboConstants.READONLY, True)
    mbo.setFieldFlag("EX2DESCRIPTION_LONGDESCRIPTION", MboConstants.READONLY, True)