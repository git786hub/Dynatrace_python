# AUTOSCRIPT NAME: CG_MSASSET
# CREATEDDATE: 2012-06-26 08:48:10
# CREATEDBY: UHD0
# CHANGEDATE: 2016-02-17 16:47:34
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

newlocation = mbo.getString("NEWLOCATION")
if ( newlocation == "" or newlocation is None ) and mbo.getString("SITEID") == "MS" :
  setError("system","requireValue")

userInfo = mbo.getUserInfo()
personid=mbo.getUserInfo().getPersonId()
groupuserSet=maximo.getMboSet("PERSONGROUPTEAM",userInfo)
groupuserSet.setWhere("PERSONGROUP ='MSASSETM' and respparty='"+personid+"'");
locationSet=maximo.getMboSet("LOCATIONS",userInfo)
locationSet.setWhere("LOCATION='"+newlocation+"' and type='MSADMIN'");
if (groupuserSet.isEmpty() and not(locationSet.isEmpty())):
  setError("asset", "canNotMoveToMSADMIN")