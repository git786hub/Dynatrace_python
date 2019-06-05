# AUTOSCRIPT NAME: EX2POWKLOG
# CREATEDDATE: 2013-10-08 18:38:00
# CREATEDBY: UFQJ
# CHANGEDATE: 2017-09-25 09:38:35
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

def setError(g, e, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e
    params= p

if not onadd:
    mbo.setFieldFlag("EX2DESCRIPTION", MboConstants.READONLY, True)
    mbo.setFieldFlag("EX2DESCRIPTION_LONGDESCRIPTION", MboConstants.READONLY, True)

if onadd and mbo.getThisMboSet().getParentApp()=="PO" and mbo.getOwner().getString("STATUS") in ['CAN', 'CLOSE']:
 setError("access", "method", ["ADD", "EX2POLOG"])