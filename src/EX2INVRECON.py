# AUTOSCRIPT NAME: EX2INVRECON
# CREATEDDATE: 2017-01-20 02:18:56
# CREATEDBY: U171
# CHANGEDATE: 2017-02-28 10:00:34
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 
from java.lang import String
from psdi.security import UserInfo
from psdi.server import  MXServer
def setError(g, e, p):
        global errorgroup, errorkey, params
        errorgroup = g
        errorkey = e
        params= p

if onupdate :
 itemnum=mbo.getString("ITEMNUM")
 location=mbo.getString("LOCATION")
 concat='SR'+location
 print concat
 userid=mbo.getUserInfo().getUserName()
 server = MXServer.getMXServer() 

 groupuserset = server.getMboSet("GROUPUSER",server.getSystemUserInfo())
 groupuserset.setWhere("USERID not in (select USERID from groupuser where GROUPNAME in ('INVENTORY')) and USERID='"+userid+"' and GROUPNAME='SCMSTOREROOM'");
 if not (groupuserset.isEmpty()):
   maxuserset = server.getMboSet("PERSONGROUPTEAM",server.getSystemUserInfo()); 
   maxuserset.setWhere("RESPPARTYGROUP='"+userid+"' and persongroup='"+concat+"'");
   if (maxuserset.isEmpty()):
    setError("EX2INV","unauthorized", [itemnum , location])