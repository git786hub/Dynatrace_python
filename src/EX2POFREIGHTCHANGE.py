# AUTOSCRIPT NAME: EX2POFREIGHTCHANGE
# CREATEDDATE: 2014-02-18 17:59:55
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:04:01
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if interactive :
        if mbo.isNull("EX2FREIGHTTERMS"):
            mbo.setFieldFlag("FOB", MboConstants.REQUIRED, False)
        else:
            mbo.setFieldFlag("FOB", MboConstants.REQUIRED, True)