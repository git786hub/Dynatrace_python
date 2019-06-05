# AUTOSCRIPT NAME: EX2STOREROOMACCESS
# CREATEDDATE: 2016-02-17 16:37:38
# CREATEDBY: UFAP
# CHANGEDATE: 2016-02-17 16:37:38
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

tolocation= mbo.getString("TOSTORELOC")

InvUseSet=mbo.getMboSet("INVUSE")
InvUseMbo=InvUseSet.getMbo(0)
userInfo = mbo.getUserInfo()
personid=mbo.getUserInfo().getPersonId()
groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
groupuserSet.setWhere("GROUPNAME in ('INVENTORY','MAXADMIN') and userid='"+personid+"'")
groupuserSet1=maximo.getMboSet("PERSONGROUPTEAM",userInfo)
groupuserSet1.setWhere("PERSONGROUP ='SR"+tolocation+"' and respparty='"+personid+"'")
print '$$$$$$$$$$$$ EX2STOREROOMACCESS script checking for both storeloc'
print groupuserSet1.getWhere()
print groupuserSet.getWhere()
if (groupuserSet.count()==0 and groupuserSet1.count()==0):
  setError("Inventory", "User does not have access to selected storeroom")