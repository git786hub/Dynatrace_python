# AUTOSCRIPT NAME: EX2WORKORDER
# CREATEDDATE: 2014-01-15 08:19:38
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-03-05 03:21:08
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants
from java.lang import String
from psdi.security import UserInfo
from psdi.server import  MXServer

userid=mbo.getUserInfo().getUserName()
server = MXServer.getMXServer() 
curstat = mbo.getString("STATUS")

if app in ["PLUSDWOTRK"]:
   if not onadd:
      mbo.setFieldFlag("EX2DERNUM", MboConstants.READONLY, True)
      mbo.setFieldFlag("CG_PROJNO", MboConstants.READONLY, True)
      if interactive and curstat == "APPR" :
         groupuserset = server.getMboSet("GROUPUSER",server.getSystemUserInfo())
         groupuserset.setWhere("USERID in (select USERID from groupuser where GROUPNAME in ('INVACCT')) and USERID='"+userid+"' ");
         if not (groupuserset.isEmpty()):
            mbo.setFieldFlag("GLACCOUNT", MboConstants.READONLY,False)