# AUTOSCRIPT NAME: EX2INVBAL1
# CREATEDDATE: 2016-11-09 02:31:21
# CREATEDBY: U03V
# CHANGEDATE: 2017-02-16 00:09:35
# CHANGEBY: U171
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

itemnum=mbo.getString("ITEMNUM")
location=mbo.getString("LOCATION")
concat='SR'+location
print concat
userid=mbo.getUserInfo().getUserName()
server = MXServer.getMXServer() 

groupuserset = server.getMboSet("GROUPUSER",server.getSystemUserInfo())
groupuserset.setWhere("USERID='"+userid+"' and GROUPNAME='SCMSTOREROOM'");
if not (groupuserset.isEmpty()):
  maxuserset = server.getMboSet("PERSONGROUPTEAM",server.getSystemUserInfo()); 
  maxuserset.setWhere("RESPPARTYGROUP='"+userid+"' and persongroup='"+concat+"'");
  if (maxuserset.isEmpty()):
   setError("EX2INV","unauthorized", [itemnum, location])