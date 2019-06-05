# AUTOSCRIPT NAME: INVENTORYSTORELOC
# CREATEDDATE: 2016-02-17 16:39:08
# CREATEDBY: UFAP
# CHANGEDATE: 2016-02-17 16:39:08
# CHANGEBY: UFAP
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.server import MXServer
maximo = MXServer.getMXServer()

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e

location= mbo.getString("STORELOC")
userInfo = mbo.getUserInfo()
personid=mbo.getUserInfo().getPersonId()
groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
groupuserSet.setWhere("GROUPNAME in ('INVENTORY','MAXADMIN') and userid='"+personid+"'")
groupuserSet1=maximo.getMboSet("PERSONGROUPTEAM",userInfo)
groupuserSet1.setWhere("PERSONGROUP='SR"+location+ "'  and respparty='"+personid+"'")
print '$$$$$$$$$$$$'
print groupuserSet1.getWhere()
print groupuserSet.getWhere()
if (groupuserSet.count()==0 and groupuserSet1.count()==0):
  setError("Inventory", "User Does not have access to selected storeroom")