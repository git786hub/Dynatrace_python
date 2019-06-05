# AUTOSCRIPT NAME: CG_CHARREAD
# CREATEDDATE: 2014-07-23 00:06:29
# CREATEDBY: UVX3
# CHANGEDATE: 2014-07-23 00:06:29
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.server import MXServer
maximo = MXServer.getMXServer()

userInfo = mbo.getUserInfo()
personid=mbo.getUserInfo().getPersonId()
groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
groupuserSet.setWhere("GROUPNAME  in ('TRNADMIN','MSPADMIN','TRNFIELD2') and userid='"+personid+"'");
if not (groupuserSet.isEmpty()):
  lastreading= mbo.getString("LASTREADINGDATE")
  if (lastreading):
    mbo.setFieldFlag("LASTREADINGDATE",MboConstants.READONLY, False);