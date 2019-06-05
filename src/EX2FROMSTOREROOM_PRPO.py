# AUTOSCRIPT NAME: EX2FROMSTOREROOM_PR/PO
# CREATEDDATE: 2016-02-02 11:28:48
# CREATEDBY: UFAP
# CHANGEDATE: 2017-06-22 01:59:29
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.app.po import PORemote
from psdi.app.pr import PRRemote
from psdi.server import MXServer
from psdi.app.inventory import MatRecTransRemote

maximo = MXServer.getMXServer()

errmsg = ''
def setError(g, k):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k

if (isinstance(mbo,PRRemote) or isinstance(mbo,PORemote)) :
    if mbo.getBoolean("INTERNAL"):
      userInfo = mbo.getUserInfo()
      personid=mbo.getUserInfo().getPersonId()
      groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
      groupuserSet.setWhere("GROUPNAME in ('INVENTORY','METERSHOP','METERSHOP2','ADMIN','ADMIN2','MAXADMIN','AP','IVTOLERANCE','IVTOL4CMDTY','RBAWFADMIN','MAXADMDIS','MAXADMTRN','SCMADMIN','SERVICECOORD') and userid='"+personid+"'")
      groupuserSet1=maximo.getMboSet("PERSONGROUPTEAM",userInfo)
      groupuserSet1.setWhere("PERSONGROUP ='SR"+storeloc+ "' and respparty='"+personid+"'")
      print '$$$$$$$$$$$$ in PR/PO APp'
      print groupuserSet1.getWhere()
      print groupuserSet.getWhere()
      if (groupuserSet.count()==0 and groupuserSet1.count()==0):
        setError("Inventory", "User Does not have access to selected storeroom")

if (isinstance(mbo,MatRecTransRemote)) :
  if(not mbo.isNull("TOSTORELOC"))  and mbo.getString("ISSUETYPE")not in ['SHIPTRANSFER']:
    userInfo = mbo.getUserInfo()
    locationsSet=maximo.getMboSet("LOCATIONS",userInfo)
    locationsSet.setWhere("LOCATION in ('"+storeloc+"')");
    if locationsSet is not None:
     locationmbo= locationsSet.getMbo(0)
     locationtype=locationmbo.getString("TYPE")
     if(locationtype=="STOREROOM"):
      personid=mbo.getUserInfo().getPersonId()
      groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
      groupuserSet.setWhere("GROUPNAME in ('INVENTORY','METERSHOP','METERSHOP2','ADMIN','ADMIN2','MAXADMIN','AP','IVTOLERANCE','IVTOL4CMDTY','RBAWFADMIN','MAXADMDIS','MAXADMTRN','SCMADMIN','SERVICECOORD') and userid='"+personid+"'")
      groupuserSet1=maximo.getMboSet("PERSONGROUPTEAM",userInfo)
      groupuserSet1.setWhere("PERSONGROUP ='SR"+storeloc+ "' and respparty='"+personid+"'")
      print app
      print '$$$$$$$$$$$$ in PR/PO APp'
      print groupuserSet1.getWhere()
      print groupuserSet.getWhere()
      if (groupuserSet.count()==0 and groupuserSet1.count()==0):
        setError("Inventory", "User Does not have access to selected storeroom")