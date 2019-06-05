# AUTOSCRIPT NAME: EX2WOMAN
# CREATEDDATE: 2018-10-31 23:47:29
# CREATEDBY: U4B0
# CHANGEDATE: 2018-12-10 13:00:28
# CHANGEBY: UGVD
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 
from psdi.server import MXServer
maximo = MXServer.getMXServer()
appName = mbo.getThisMboSet().getParentApp()
failureCode = mbo.getString("FAILURECODE")
istask = mbo.getBoolean("ISTASK")
cg_worktype = mbo.getString("CG_WORKTYPE")
if interactive  and appName == 'WOT_TRN' and failureCode in ('BREAKER','PWRXFMR') and cg_worktype=="PREVENTIVE" and not istask: 
 curstat = mbo.getString("STATUS")
 userInfo = mbo.getUserInfo()
 personid=mbo.getUserInfo().getPersonId()
 groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
 groupuserSet.setWhere("GROUPNAME in ('TRNADMIN','MSPADMIN','TRNBROWSE') and userid='"+personid+"'")
 groupuserSet1=maximo.getMboSet("GROUPUSER",userInfo)
 groupuserSet1.setWhere("GROUPNAME in ('TRNBROWSE') and userid='"+personid+"'")
 if curstat =='COMP':  
  if(groupuserSet.isEmpty()):
   mbo.setFieldFlag("EX2WOL2", MboConstants.REQUIRED, True)
   mbo.setFieldFlag("EX2WOL3", MboConstants.REQUIRED, True)
  if(not(groupuserSet1.isEmpty())):
   mbo.setFieldFlag("EX2WOL2", MboConstants.READONLY,True)
   mbo.setFieldFlag("EX2WOL3", MboConstants.READONLY,True)