# AUTOSCRIPT NAME: EX2INVDEFAULT
# CREATEDDATE: 2015-09-02 07:23:48
# CREATEDBY: UVX3
# CHANGEDATE: 2017-04-08 11:21:24
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.security import UserInfo
from psdi.server import  MXServer

if launchPoint == 'EX2INVDEFAULT':
     mbo.setValue("CCF",'365',MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
     mbo.setValue("MINLEVEL",'-1',MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
     mbo.setValue("DELIVERYTIME",'14',MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)

if onadd and launchPoint == 'EX2INVDEFAULT':
 userid=mbo.getUserInfo().getUserName()
 server = MXServer.getMXServer() 

 groupuserset = server.getMboSet("GROUPUSER",server.getSystemUserInfo())
 groupuserset.setWhere("USERID='"+userid+"' and GROUPNAME='SCMSTOREROOM'");
 if not (groupuserset.isEmpty()):
   mbo.setValue("REORDER",'0',MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)

     
#invbalset= mbo.getMboSet("INVBALANCES")
#invbal = invbalset.add()
#invbal.setValue("BINNUM",mbo.getString("BINNUM"))

if onadd and mbo.isNull("RECEIPTTOLERANCE"):
    mbo.setValue("RECEIPTTOLERANCE",35, MboConstants.NOACCESSCHECK)