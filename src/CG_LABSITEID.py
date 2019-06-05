# AUTOSCRIPT NAME: CG_LABSITEID
# CREATEDDATE: 2015-07-15 03:07:44
# CREATEDBY: UVX3
# CHANGEDATE: 2015-07-16 03:06:20
# CHANGEBY: URE7
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p

siteid= mbo.getString("siteid")
transtype=mbo.getString("TRANSTYPE")


if(siteid=='DIS' and transtype=='NON-WORK'):
   setError("labor", "siteid", None)