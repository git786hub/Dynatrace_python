# AUTOSCRIPT NAME: EX2POLINEPERVAL
# CREATEDDATE: 2016-12-19 11:11:35
# CREATEDBY: U171
# CHANGEDATE: 2016-12-21 02:14:44
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 
from psdi.tloam.app.po import PORemote
from psdi.server import MXServer

ex2invapprMboSet = None

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p

#1
ex2invapprmbo = mbo.getString("EX2INVAPPR")
ex2powappr = mbo.getMboSet("EX2POWAPPR")
ex2invapprMboSet = None
ex2invapprMboSet = mbo.getMboSet("EX2INVAPPR")

if launchPoint =='EX2INVAPPR':
   if ex2invapprmbo <> "" and ex2invapprMboSet.count() < 1 :
      p = ["Invoice Approver"]      
      setError("ex2_person", "DoesNotExist", p)

if ex2invapprmbo <> "" and ex2powappr.count() > 0 : 
   ex2inactiveinvapprMboSet = mbo.getMboSet("EX2INVAPPRACTIVE")
   if ex2inactiveinvapprMboSet.count() > 0:   
      p = ["Invoice Approver"]
      setError("ex2_inactper", "inactPer", p)

#2
supervisormbo = mbo.getString("SUPERVISOR")
#ex2powappr = mbo.getMboSet("EX2POWAPPR")
supervisorMboSet = None
supervisorMboSet = mbo.getMboSet("EX2SUPERVISOR")

if launchPoint =='SUPERVISOR':
   if supervisormbo <> "" and supervisorMboSet.count() < 1 :
      p = ["Supervisor"]      
      setError("ex2_person", "DoesNotExist", p)

if supervisormbo <> "" and ex2powappr.count() > 0 : 
   ex2inactiveSupMboSet = mbo.getMboSet("EX2SUPACTIVE")
   if ex2inactiveSupMboSet.count() > 0:   
      p = ["Supervisor"]
      setError("ex2_inactper", "inactPer", p)
#mbo.setValue("REMARK",mbo.getString("EX2INVAPPR"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)