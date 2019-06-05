# AUTOSCRIPT NAME: EX2_EDITCONTREFNUM
# CREATEDDATE: 2018-04-09 02:22:47
# CREATEDBY: U1MZ
# CHANGEDATE: 2018-04-16 02:00:57
# CHANGEBY: U1LI
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.app.pr import PRRemote
from psdi.server import MXServer

maximo = MXServer.getMXServer()
pr=mbo.getOwner()


userInfo = mbo.getUserInfo()
personid=mbo.getUserInfo().getPersonId()
groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
groupuserSet.setWhere("GROUPNAME  in ('BUYER') and userid='"+personid+"'")


if(pr and isinstance(pr,PRRemote)):
    if (launchPoint == 'EX2_EDITCONTREFNUM' ):
        if (pr.getString("STATUS") in ["IWAPPR","BWAPPR","WAPPR"]):
             if (not (groupuserSet.isEmpty())):
                mbo.setFieldFlag("CONTRACTREFNUM", MboConstants.READONLY, False)
                pr.setFieldFlag("CONTRACTREFNUM", MboConstants.READONLY, False)
             else:
                mbo.setFieldFlag("CONTRACTREFNUM", MboConstants.READONLY, True)
                pr.setFieldFlag("CONTRACTREFNUM", MboConstants.READONLY, True)