# AUTOSCRIPT NAME: CG_STATUSCAN
# CREATEDDATE: 2014-12-05 00:43:38
# CREATEDBY: UVX3
# CHANGEDATE: 2014-12-16 14:03:49
# CHANGEBY: UFAP
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

StatusMboSet=mbo.getMboSet("CG_STATUSERROR")
num=StatusMboSet.count()

if(num>0):
  
  Status= mbo.getString("STATUS")
  StatusMbo = StatusMboSet.getMbo(0)

  if(Status=='CANCELLED'):
    setError("STATUSERR", "INVSTATUS", None)