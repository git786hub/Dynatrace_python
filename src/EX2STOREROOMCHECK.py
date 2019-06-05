# AUTOSCRIPT NAME: EX2STOREROOMCHECK
# CREATEDDATE: 2016-02-02 13:19:57
# CREATEDBY: UFAP
# CHANGEDATE: 2017-06-22 01:49:43
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

if ( not mbo.isNull("TOSTORELOC")) :
  if mbo.getString("ISSUETYPE") in ['SHIPTRANSFER']:
   storeloc=mbo.getString("FROMSTORELOC")
  else:
   storeloc=mbo.getString("TOSTORELOC")
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
    print '$$$$$$$$$$$$ in Receving App'
    print groupuserSet1.getWhere()
    print groupuserSet.getWhere()
    if (groupuserSet.count()==0 and groupuserSet1.count()==0):
      setError("Inventory", "User Does not have access to selected storeroom "+storeloc)