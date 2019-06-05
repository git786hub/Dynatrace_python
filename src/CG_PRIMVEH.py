# AUTOSCRIPT NAME: CG_PRIMVEH
# CREATEDDATE: 2018-07-12 09:40:19
# CREATEDBY: U3LO
# CHANGEDATE: 2018-07-18 02:53:38
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from java.lang import String
from psdi.security import UserInfo
from psdi.server import  MXServer

userid=mbo.getUserInfo().getUserName()
server = MXServer.getMXServer() 


def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p
mCount = mbo.getThisMboSet().count()
groupuserset = server.getMboSet("GROUPUSER",server.getSystemUserInfo())
groupuserset.setWhere("USERID in (select USERID from groupuser where GROUPNAME in ('TRNCORRECTOR')) and USERID='"+userid+"' ");
pvehSet = mbo.getMboSet("CG_ITEMSTATUS")
if not (groupuserset.isEmpty()):
   if (onadd or onupdate):
      if mCount > 1 or pvehSet.getMbo(0).getString("STATUS") <> 'ACTIVE':
         setError("labor", "privehicle", None)