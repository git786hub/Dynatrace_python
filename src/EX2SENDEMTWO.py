# AUTOSCRIPT NAME: EX2SENDEMTWO
# CREATEDDATE: 2014-04-17 18:20:14
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-04-22 13:31:12
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.iface.mic import MicService
from psdi.server import MXServer
from psdi.mbo import MboConstants

cWO = mbo.getInt("WORKORDERID")

micSrv = MXServer.getMXServer().lookup("MIC")

micSrv.exportData("EX2WOInterface", "EX2EMTSYS", "workorderid='"+str(cWO)+"'", micSrv.getNewUserInfo() , 1)