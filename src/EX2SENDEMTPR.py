# AUTOSCRIPT NAME: EX2SENDEMTPR
# CREATEDDATE: 2014-03-17 12:57:14
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-10-13 20:20:23
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.iface.mic import MicService
from psdi.server import MXServer
from psdi.mbo import MboConstants

cPRNum = mbo.getString("PRNUM")
cSiteid = mbo.getString("SITEID")

micSrv = MXServer.getMXServer().lookup("MIC")

micSrv.exportData("EX2PRInterface", "EX2EMTSYS", "siteid='"+cSiteid+"' and prnum='"+cPRNum+"'", micSrv.getNewUserInfo() , 1)