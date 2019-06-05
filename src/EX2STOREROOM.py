# AUTOSCRIPT NAME: EX2STOREROOM
# CREATEDDATE: 2016-09-01 06:13:53
# CREATEDBY: U171
# CHANGEDATE: 2017-12-05 03:14:25
# CHANGEBY: U144
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.server import MXServer
maximo = MXServer.getMXServer()

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e

storeloc= mbo.getString("STORELOC")
userInfo = mbo.getUserInfo()
personid=mbo.getUserInfo().getPersonId()
groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
groupuserSet.setWhere("GROUPNAME in ('INVENTORY','MAXADMIN') and userid='"+personid+"'")
groupuserSet1=maximo.getMboSet("PERSONGROUPTEAM",userInfo)
groupuserSet1.setWhere("PERSONGROUP ='SR"+storeloc+ "' and respparty='"+personid+"'")
print '$$$$$$$$$$$$'
print groupuserSet1.getWhere()
print groupuserSet.getWhere()
if (groupuserSet.count()==0 and groupuserSet1.count()==0):
  setError("Inventory", "User does not have access to selected storeroom")