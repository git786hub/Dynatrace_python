# AUTOSCRIPT NAME: EX2STATUSCAN
# CREATEDDATE: 2015-04-10 01:15:53
# CREATEDBY: UVX3
# CHANGEDATE: 2015-04-10 11:05:53
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

if(interactive) : 

  StatusMboSet=mbo.getMboSet("EX2STATUSERROR")
  num=StatusMboSet.count()

  if(num>0):
  
    Status= mbo.getString("STATUS")
    StatusMbo = StatusMboSet.getMbo(0)

    if(Status=='CANCELLED'):
      setError("STATUSERR", "INVSTATUS", None)