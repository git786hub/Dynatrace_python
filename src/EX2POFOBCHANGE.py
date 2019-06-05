# AUTOSCRIPT NAME: EX2POFOBCHANGE
# CREATEDDATE: 2014-02-18 17:38:37
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:03:59
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if interactive :
        if mbo.isNull("FOB"):
            mbo.setFieldFlag("EX2FREIGHTTERMS", MboConstants.REQUIRED, False)
        else:
            mbo.setFieldFlag("EX2FREIGHTTERMS", MboConstants.REQUIRED, True)