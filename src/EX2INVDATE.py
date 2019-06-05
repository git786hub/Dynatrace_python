# AUTOSCRIPT NAME: EX2INVDATE
# CREATEDDATE: 2014-08-06 01:09:13
# CREATEDBY: UQRM
# CHANGEDATE: 2014-08-06 01:09:13
# CHANGEBY: UQRM
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from java.util import Date
from psdi.util import MXApplicationException

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e

sysdate = Date()
invdate = mbo.getDate("INVOICEDATE")
if invdate is not None and invdate <> "" : 
    if invdate > sysdate:
        #setError("invoice", "NoFutureDate")
        warning = MXApplicationException("invoice", "NoFutureDate")
        mbo.getThisMboSet().addWarning(warning)